from pathlib import Path
import contextlib, io, json, runpy, warnings
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT=Path('tmp/pdfs/audit-20261027/code')
original=Path('coala-book-md/vibe-coding-16/examples/source-based/ch13-scatter.py').read_text(encoding='utf-8')
preamble='''from matplotlib import font_manager

font_names = {font.name for font in
              font_manager.fontManager.ttflist}
for name in ("Malgun Gothic", "AppleGothic",
             "Noto Sans CJK KR", "NanumGothic"):
    if name in font_names:
        plt.rcParams["font.family"] = name
        break
else:
    raise RuntimeError("Install a Korean font, then rerun.")
plt.rcParams["axes.unicode_minus"] = False
'''
new=original.replace('import matplotlib.pyplot as plt\n','import matplotlib.pyplot as plt\n'+preamble)
candidate=OUT/'ch13-scatter-font-candidate.py'
candidate.write_text(new,encoding='utf-8')
plt.rcdefaults()
plt.show=lambda: plt.gcf().savefig(OUT/'ch13-scatter-font-candidate.png',dpi=120)
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter('always')
    ns=runpy.run_path(str(candidate))
assert not caught, [str(w.message) for w in caught]
ax=plt.gca()
assert ax.get_xlabel()=='X축 제목' and ax.get_ylabel()=='Y축 제목'
print('candidate passed, selected font:', plt.rcParams['font.family'], 'warnings:',len(caught))
(OUT/'font-candidate-result.json').write_text(json.dumps({'candidate':str(candidate),'font':plt.rcParams['font.family'],'warnings':len(caught),'xlabel':ax.get_xlabel(),'ylabel':ax.get_ylabel()},ensure_ascii=False,indent=2),encoding='utf-8')
