import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { parseArgs } from 'node:util';

const root = path.resolve(import.meta.dirname, '..');
const runtime = 'C:/Users/use/.cache/codex-runtimes/codex-primary-runtime/dependencies';
const modules = path.join(runtime, 'node/node_modules');
process.env.RUNTIME_NODE_MODULES = modules;
const { Presentation, PresentationFile } = await import(pathToFileURL(path.join(modules, '@oai/artifact-tool/dist/artifact_tool.mjs')).href);
const { FontLibrary } = await import(pathToFileURL(path.join(modules, '@oai/artifact-tool/node_modules/skia-canvas/lib/index.js')).href);
FontLibrary.use('Wanted Sans', [path.join(root,'tmp/pdfs/fonts/WantedSans-Regular.ttf'),path.join(root,'tmp/pdfs/fonts/WantedSans-Medium.ttf'),path.join(root,'tmp/pdfs/fonts/WantedSans-Bold.ttf')]);

const {values:args} = parseArgs({options:{scene:{type:'string'},output:{type:'string'}}});
const scenePath = path.resolve(args.scene ?? path.join(root,'tmp/pptx/textbook/scene.json'));
const tmp = path.dirname(scenePath);
const scene = JSON.parse(await fs.readFile(scenePath,'utf8'));
const scale = 4/3;
const presentation = Presentation.create({slideSize:{width:scene.width*scale,height:scene.height*scale}});
const nativeTables=[];
const maxPages=process.env.PPTX_SAMPLE ? Number(process.env.PPTX_SAMPLE) : scene.pages.length;

function pos(o) {return {left:o.left*scale,top:o.top*scale,width:o.width*scale,height:o.height*scale};}
function addText(slide,o) {
  if (!o.text) return;
  // A one-line textbox retains the exact wrapping decisions of the PDF source.
  const available=scene.width-o.left-4;
  const width=Math.min(available,Math.max(o.width+12,o.size*1.1));
  const height=o.size*1.55;
  const shape=slide.shapes.add({geometry:'textbox',position:pos({...o,width,height}),fill:'none',line:{fill:'none',width:0}});
  shape.text=o.text;
  shape.text.style={fontSize:o.size*scale,typeface:o.font==='Code'?'Consolas':'Wanted Sans',bold:o.font==='WantedBold',color:o.color,wrap:'none',autoFit:'none',insets:0,verticalAlignment:'top'};
}
function addTable(slide,o,index) {
  const b=o.block;
  const rows=[{cells:b.headers,height:b.headHeight},...b.rows];
  const table=slide.tables.add({rows:rows.length,columns:b.cols.length,left:34*scale,top:b.y*scale,width:b.cols.reduce((a,v)=>a+v,0)*scale,height:b.height*scale,columnWidths:b.cols.map(v=>v*scale),values:rows.map(row=>row.cells.map(lines=>lines.join('\n')))});
  nativeTables.push(index+1);
  table.borders.assign({fill:'#DDE3EC',width:.65*scale,style:'solid'});
  for (let r=0;r<rows.length;r++) {
    table.rows[r].height=rows[r].height*scale;
    for(let c=0;c<b.cols.length;c++) {
      const cell=table.getCell(r,c);
      cell.fill=r===0?'#EAF1FF':r%2===0?'#F8FAFD':'#FFFFFF';
      cell.text.style={fontSize:14*scale,typeface:'Wanted Sans',bold:r===0,color:r===0?'#1800AD':'#151515',wrap:'none',autoFit:'none',insets:{top:11*scale,bottom:11*scale,left:12*scale,right:12*scale},verticalAlignment:'top',lineSpacing:2};
    }
  }
}
for (let index=0;index<maxPages;index++) {
  const slide=presentation.slides.add();
  slide.background.fill='#FFFFFF';
  slide.speakerNotes.text=`${scene.titles[index]}\n출처: AI와 함께하는 바이브 코딩 교재, ${index+1}쪽`;
  for (const o of scene.pages[index]) {
    if (o.kind==='text') addText(slide,o);
    else if(o.kind==='table') addTable(slide,o,index);
    else if(o.kind==='image') {
      slide.images.add({blob:new Uint8Array(await fs.readFile(o.path)),contentType:'image/png',position:pos(o),fit:'contain',alt:path.basename(o.path)});
    } else if(o.kind==='line') {
      slide.shapes.add({geometry:'line',position:{left:Math.min(o.x1,o.x2)*scale,top:Math.min(o.y1,o.y2)*scale,width:Math.max(.01,Math.abs(o.x2-o.x1))*scale,height:Math.max(.01,Math.abs(o.y2-o.y1))*scale},fill:'none',line:{fill:o.stroke,width:o.lineWidth*scale,style:'solid'}});
    } else {
      // Page white is already represented by the slide background.
      if(o.left===0&&o.top===0&&Math.abs(o.width-scene.width)<.01&&o.fill==='#FFFFFF') continue;
      slide.shapes.add({geometry:o.kind,position:pos(o),fill:o.fill,line:{fill:o.stroke,width:o.stroke==='none'?0:o.lineWidth*scale,style:'solid'},...(o.radius?{borderRadius:o.radius*scale}:{})});
    }
  }
  if((index+1)%20===0) console.log(`authored ${index+1}/${maxPages}`);
}
await fs.mkdir(tmp,{recursive:true});
await fs.mkdir(path.dirname(path.resolve(args.output ?? path.join(root,'output/pptx/vibe-coding-16-upstream.pptx'))),{recursive:true});
const candidate=path.join(tmp,process.env.PPTX_SAMPLE?'sample.pptx':'candidate.pptx');
await (await PresentationFile.exportPptx(presentation)).save(candidate);
console.log(`exported ${candidate}`);
const renderIndices=process.env.PPTX_SAMPLE ? [...Array(maxPages).keys()] : [...Array(maxPages).keys()];
await fs.mkdir(path.join(tmp,'renders'),{recursive:true});
for(const index of renderIndices) {
  const png=await presentation.export({slide:presentation.slides.items[index],format:'png',scale:1});
  await fs.writeFile(path.join(tmp,'renders',`slide-${String(index+1).padStart(3,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
  if((index+1)%20===0) console.log(`rendered ${index+1}/${maxPages}`);
}
// Finalize in a fresh process after the renderer releases its native buffers.
// node scripts/finalize_textbook_pptx.mjs
console.log(`Candidate and PNG renders ready; finalize with --scene ${scenePath}${args.output ? ` --output ${args.output}` : ''}.`);
