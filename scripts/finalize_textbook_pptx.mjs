import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { parseArgs } from 'node:util';
const root=path.resolve(import.meta.dirname,'..');
const runtime='C:/Users/use/.cache/codex-runtimes/codex-primary-runtime/dependencies';
process.env.RUNTIME_NODE_MODULES=path.join(runtime,'node/node_modules');
const skill='C:/Users/use/.codex/plugins/cache/openai-primary-runtime/presentations/26.1020.11348/skills/presentations';
const {values:args}=parseArgs({options:{scene:{type:'string'},output:{type:'string'},candidate:{type:'string'}}});
const scenePath=path.resolve(args.scene ?? path.join(root,'tmp/pptx/textbook/scene.json'));
const tmp=path.dirname(scenePath);
const finalPath=path.resolve(args.output ?? path.join(root,'output/pptx/vibe-coding-16-upstream.pptx'));
const scene=JSON.parse(await fs.readFile(scenePath,'utf8'));
const owners=scene.pages.map((p,i)=>p.some(o=>o.kind==='table')?i+1:null).filter(Boolean);
try {
  const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
  console.log('starting finalizer');
  const result=await finalizePresentation({workspaceDir:root,candidatePath:path.resolve(args.candidate ?? path.join(tmp,'candidate.pptx')),finalPath,pythonExecutable:path.join(runtime,'python/python.exe'),integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu',`${Math.round(scene.width*12700)},${Math.round(scene.height*12700)}`,'--validate-bullet-geometry','--validate-heading-fit',...owners.flatMap(n=>['--require-native-table-slide',String(n)])],explicitTotalSlideCount:scene.pages.length,requiredNativeTableOwnerSlides:owners,requiredNativeChartOwnerSlides:[],fontPolicy:{basis:'design',families:['Wanted Sans','Consolas']},verifyArtifactToolImport:true,receiptPath:path.join(tmp,'validation.json')});
  console.log(JSON.stringify(result));
} catch(error) {
  console.error('FINALIZER ERROR',error);
  console.error(JSON.stringify(error,Object.getOwnPropertyNames(error),2));
  process.exitCode=1;
}
