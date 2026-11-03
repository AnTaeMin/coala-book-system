import contextlib, hashlib, io, json, re, runpy, sys, warnings
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
ROOT=Path.cwd()
OUT=ROOT/'tmp/pdfs/audit-20261027/code'
BOOK=ROOT/'coala-book-md/vibe-coding-16'
text='\n'.join((BOOK/f'ch{i:02d}.md').read_text(encoding='utf-8') for i in (12,13))
blocks={}
for match in re.finditer(r':::page\{[^\n]*id="([^"]+)"[^\n]*\}\n(.*?)(?=\n:::\s*(?:\n|$))',text,re.S):
    code=re.search(r'```python\n(.*?)\n```',match[2],re.S)
    if code: blocks[match[1]]=code[1]
results=[]
for f in sorted((BOOK/'examples/source-based').glob('*.py')):
    plt.rcdefaults()
    code=f.read_text(encoding='utf-8').rstrip()
    assert blocks[f.stem]==code, 'manuscript mismatch '+f.name
    # Also compile the exact block extracted from the final target PDF (handled separately).
    plt.close('all')
    figures=[]
    def save(*args,**kwargs):
        figures.append(plt.gcf())
        plt.gcf().savefig(OUT/(f.stem+'.png'), dpi=120)
    old_show=plt.show
    plt.show=save
    capture=io.StringIO()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        with contextlib.redirect_stdout(capture):
            ns=runpy.run_path(str(f))
    plt.show=old_show
    assert len(figures)==1
    ax=figures[0].axes[0]
    semantic={}
    if f.stem=='ch12-one-array':
        line=ax.lines[0]; assert list(line.get_xdata())==list(range(5)); assert list(line.get_ydata())==[1,2,3,4,5]
        semantic={'x':list(map(float,line.get_xdata())), 'y':list(map(float,line.get_ydata()))}
    elif f.stem=='ch12-two-arrays':
        line=ax.lines[0]; assert list(line.get_xdata())==[15,25,35,45,55]; assert list(line.get_ydata())==[5,10,15,20,25]
        semantic={'x':list(map(float,line.get_xdata())), 'y':list(map(float,line.get_ydata()))}
    elif f.stem=='ch12-range':
        line=ax.lines[0]; assert list(line.get_xdata())==[1,2,3,4,5]; assert list(line.get_ydata())==[5,10,15,20,25]; assert line.get_marker()=='+'; assert line.get_color()=='b'; assert tuple(ax.get_xlim())==(0,10); assert tuple(ax.get_ylim())==(0,25)
        semantic={'marker':line.get_marker(),'color':line.get_color(),'xlim':list(ax.get_xlim()),'ylim':list(ax.get_ylim())}
    elif f.stem=='ch12-markers':
        line=ax.lines[0]; assert line.get_marker()=='o'; assert line.get_color()=='r'; assert line.get_linestyle()=='None'; assert ax.get_xlabel()=='x'; assert ax.get_ylabel()=='y'; assert ax.get_title()=='hello'; assert any(t.get_text()=='12/19' and t.get_position()==(3,5) for t in ax.texts)
        semantic={'marker':line.get_marker(),'color':line.get_color(),'linestyle':line.get_linestyle(),'annotation':'12/19 at (3,5)'}
    elif f.stem=='ch13-bars':
        heights=[r.get_height() for r in ax.patches]; assert heights==[1,2,4,8,16,32,64,128]; assert len(ax.patches)==8
        semantic={'heights':heights}
    elif f.stem=='ch13-grouped':
        assert len(ax.patches)==10; heights=[r.get_height() for r in ax.patches]; assert heights==[35,80,84,83,50,73,80,77,40,86]
        centers=[r.get_x()+r.get_width()/2 for r in ax.patches]; assert np.allclose(centers[:5],[.8,2.8,4.8,6.8,8.8]); assert np.allclose(centers[5:],[1.6,3.6,5.6,7.6,9.6]); assert np.allclose(ax.get_xticks(),[1.2,3.2,5.2,7.2,9.2]); assert [t.get_text() for t in ax.get_xticklabels()]==['one','two','three','four','five']
        semantic={'heights':heights,'centers':centers,'ticks':list(ax.get_xticks())}
    elif f.stem=='ch13-scatter':
        offsets=np.asarray(ax.collections[0].get_offsets()); x=offsets[:,0]; y=offsets[:,1]
        assert len(x)==20; assert np.allclose(x,np.arange(1.1,100.,5.)); assert np.all(y>=x*1.5); assert np.all(y<x*1.5+50)
        np.random.seed(20211206); expected=x*1.5+np.random.rand(20)*50; assert np.allclose(y,expected)
        assert ax.get_xlabel()=='X축 제목'; assert ax.get_ylabel()=='Y축 제목'; assert ax.get_title()=='random'; assert [t.get_text() for t in ax.get_legend().get_texts()]==['random']
        semantic={'points':len(x),'first_point':offsets[0].tolist(),'last_point':offsets[-1].tolist(),'seed_repeatability':True,'labels':[ax.get_xlabel(),ax.get_ylabel()]}
    results.append({'file':f.name,'status':'passed','code_sha256':hashlib.sha256(code.encode()).hexdigest(),'stdout':capture.getvalue(),'semantics':semantic,'warnings':sorted(set(str(w.message) for w in caught))})
    plt.close('all')
# Simulate a machine where no supported Korean family is installed.
plt.rcdefaults()
original_fonts=font_manager.fontManager.ttflist
candidate_names={'Malgun Gothic','AppleGothic','Noto Sans CJK KR','Noto Sans KR','NanumGothic','Wanted Sans'}
font_manager.fontManager.ttflist=[f for f in original_fonts if f.name not in candidate_names]
plt.show=lambda: plt.gcf().savefig(OUT/'ch13-scatter-no-korean-font.png',dpi=120)
try:
    with warnings.catch_warnings(record=True) as fallback_warnings:
        warnings.simplefilter('always')
        fallback_namespace=runpy.run_path(str(BOOK/'examples/source-based/ch13-scatter.py'))
    fallback_axis=plt.gca()
    assert fallback_namespace['font_name'] is None
    assert fallback_axis.get_xlabel()=='X axis'
    assert fallback_axis.get_ylabel()=='Y axis'
    assert len(fallback_axis.collections[0].get_offsets())==20
    assert not fallback_warnings, [str(w.message) for w in fallback_warnings]
    fallback={'status':'passed','selected_korean_font':None,'xlabel':fallback_axis.get_xlabel(),'ylabel':fallback_axis.get_ylabel(),'warnings':[],'points':20}
finally:
    font_manager.fontManager.ttflist=original_fonts
    plt.close('all')
assert all(not r['warnings'] for r in results), 'Unexpected example warnings'
report={'korean_font_fallback':fallback,'python':sys.version.split()[0],'runtime':sys.executable,'matplotlib':matplotlib.__version__,'numpy':np.__version__,'executed':len(results),'semantic_checks_passed':len(results),'blocks_match_files':True,'available_korean_fonts':sorted(set(x.name for x in font_manager.fontManager.ttflist if any(y in x.name.lower() for y in ['malgun','noto sans kr','wanted','nanum','applegothic']))),'records':results}
(OUT/'execution-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,default=lambda x: x.item()),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2,default=lambda x: x.item()))

