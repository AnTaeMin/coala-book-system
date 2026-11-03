from pathlib import Path
p=Path('tmp/pdfs/audit-20261027/code/check_examples.py')
s=p.read_text(encoding='utf-8-sig')
s=s.replace("text=(BOOK/'book.md').read_text(encoding='utf-8')", "text='\\n'.join((BOOK/f'ch{i:02d}.md').read_text(encoding='utf-8') for i in (12,13))")
s=s.replace("report={'python':", """# Simulate a machine where no supported Korean family is installed.
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
report={'korean_font_fallback':fallback,'python':""")
p.write_text(s,encoding='utf-8')
