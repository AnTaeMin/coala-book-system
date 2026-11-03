"""Move existing graph practice before Chart and remove the API practice.

Inputs come from an immutable pre-edit snapshot so chapter-prefix cycles cannot
overwrite one another. This script does not assemble or render the textbook.
"""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "coala-book-md/vibe-coding-16"
ARCHIVE = BOOK / "previous-reports/20261011-before-graph-first"
EDITION = "graph-first-16-sessions"
CHAPTER_MAP = {12: 13, 13: 14, 14: 12}
REMOVED = {"ch13-practice-api", "ch13-api-steps", "ch13-api-screen"}
REMOVED_ASSET = "assets/source-20261010/subway-top5-result.png"


def read(name):
    return (ARCHIVE / name).read_text(encoding="utf-8")


def write(name, value):
    path = BOOK / name
    assert path.resolve().is_relative_to(BOOK.resolve())
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def read_json(name):
    return json.loads(read(name))


def save_json(name, value):
    write(name, json.dumps(value, ensure_ascii=False, indent=2))


def pages(text):
    return re.findall(r":::page\{[^\n]*\}.*?\n:::", text, re.S)


def page_id(text):
    return re.search(r'\bid="([^"]+)"', text)[1]


def digest(value):
    return hashlib.sha256(value).hexdigest()


old_chapters = {number: read(f"ch{number:02d}.md") for number in range(1, 17)}
old_pages = pages(read("book.md"))
assert len(old_pages) == 170
mapping = {}
for page in old_pages:
    old_id = page_id(page)
    if old_id in REMOVED:
        mapping[old_id] = None
        continue
    match = re.match(r"ch(\d{2})-", old_id)
    if match and int(match[1]) in CHAPTER_MAP:
        old_number = int(match[1])
        new_number = CHAPTER_MAP[old_number]
        mapping[old_id] = old_id.replace(f"ch{old_number:02d}-", f"ch{new_number:02d}-", 1)
    else:
        mapping[old_id] = old_id
mapping["ch13-practice-4"] = "ch14-practice-3"
assert {key for key, value in mapping.items() if value is None} == REMOVED


def reassign(page, old_number, new_number):
    old_id = page_id(page)
    new_id = mapping[old_id]
    assert new_id is not None
    value = page.replace(f'id="{old_id}"', f'id="{new_id}"', 1)
    value = re.sub(r'\bchapter="\d+"', f'chapter="{new_number}"', value)
    value = re.sub(r"^## \d+차시 · 개념과 실습$", f"## {new_number}차시 · 개념과 실습", value, flags=re.M)
    value = re.sub(r'\bpractice="\d{3}-(\d+)"', lambda match: f'practice="{new_number:03d}-{match[1]}"', value)
    if old_id == "ch13-practice-4":
        value = value.replace('practice="014-4"', 'practice="014-3"')
    return value


# Read all old chapters before writing any chapter in the 12 -> 13 -> 14 cycle.
new_chapters = {}
for old_number, new_number in CHAPTER_MAP.items():
    text = old_chapters[old_number]
    front = text.split(":::page", 1)[0]
    front = re.sub(r"^subtitle: \d+차시", f"subtitle: {new_number}차시", front, flags=re.M)
    bodies = [reassign(page, old_number, new_number) for page in pages(text) if page_id(page) not in REMOVED]
    if old_number == 13:
        bodies[0] = bodies[0].replace(
            "- API 자료의 항목을 표·그래프에 연결하고 상위 5개를 표시할 수 있다.\n",
            "- 학교별 학생 수를 집계하여 막대그래프로 비교할 수 있다.\n"
        ).replace(
            "학생 자료를 불러와 표와 그래프로 살펴봅니다. API는 프로그램이 다른 서비스와 정보를 주고받는 연결 방식입니다. 자료를 가져온 뒤 저장하고 다시 불러오는 과정까지 확인합니다.",
            "학생 자료를 불러와 표와 그래프로 살펴봅니다. 표시할 항목을 선택하고 학교별 학생 수를 비교합니다. 자료를 저장하고 다시 불러오는 과정까지 확인합니다."
        )
        bodies[-1] = bodies[-1].replace("- [ ] API로 가져온 자료의 표·그래프를 확인했다.\n", "")
    new_chapters[new_number] = front.rstrip() + "\n\n" + "\n\n".join(bodies)

new_chapters[8] = old_chapters[8].replace(
    "# 디자이너 이름과 Python API 구분하기", "# 디자이너 이름과 Python 클래스 구분하기"
)
new_chapters[16] = old_chapters[16].replace(
    "민감한 정보와 인증키를 빼고", "이름·연락처 등 개인정보를 빼고"
).replace(
    "외부 자료를 사용하는 기능은 실제 연결 결과를 기록합니다.",
    "불러온 자료의 값과 실행 결과를 기록합니다."
)

for number, text in new_chapters.items():
    write(f"ch{number:02d}.md", text)

current_pages = []
for number in range(1, 17):
    current_pages.extend(pages((BOOK / f"ch{number:02d}.md").read_text(encoding="utf-8")))
by_id = {page_id(page): page for page in current_pages}
order = {page_id(page): index for index, page in enumerate(current_pages)}
assert len(by_id) == len(current_pages) == 166  # book-guide is assembled by root.
expected_ids = {value for value in mapping.values() if value is not None}
assert set(by_id) | {"book-guide"} == expected_ids
assert not re.search(r"\bAPI\b|인증키|지하철|자치구", "\n".join(current_pages), re.I)

practices = read_json("practice-source-map.json")
retained = []
for old_record in practices["practices"]:
    new_id = mapping[old_record["page_id"]]
    if new_id is None:
        continue
    record = deepcopy(old_record)
    record["page_id"] = new_id
    record["chapter"] = int(new_id[2:4])
    page = by_id[new_id]
    record["practice_id"] = re.search(r'\bpractice="([^"]+)"', page)[1]
    record["title"] = re.search(r"^# (.+)$", page, re.M)[1]
    record["completion_criteria"] = re.findall(r"^- \[ \] (.+)$", page, re.M)
    retained.append(record)
practices["practices"] = sorted(retained, key=lambda record: order[record["page_id"]])
practices["reviewed_date"] = "2026-10-11"
practices["edition"] = EDITION
assert len(retained) == 40
counts = Counter(record["chapter"] for record in retained)
assert {number: counts[number] for number in range(12, 17)} == {12: 8, 13: 3, 14: 3, 15: 3, 16: 1}
assert len({record["practice_id"] for record in retained}) == 40
for number in range(1, 17):
    identifiers = [record["practice_id"] for record in practices["practices"] if record["chapter"] == number]
    assert identifiers == [f"{number:03d}-{index}" for index in range(1, len(identifiers) + 1)]
save_json("practice-source-map.json", practices)

code_specs = read_json("code-specs.json")
old_code_specs = deepcopy(code_specs)
for record in code_specs:
    record["page_id"] = mapping[record["page_id"]]
    record["chapter"] = int(record["page_id"][2:4])
code_specs.sort(key=lambda record: order[record["page_id"]])
save_json("code-specs.json", code_specs)
code_results = read_json("code-results.json")
old_code_results = deepcopy(code_results)
for record in code_results["records"]:
    record["page_id"] = mapping[record["page_id"]]
    if "chapter" in record:
        record["chapter"] = int(record["page_id"][2:4])
code_results["records"].sort(key=lambda record: order[record["page_id"]])
code_results["edition"] = EDITION
save_json("code-results.json", code_results)

example_dir = BOOK / "examples/source-based"
archived_examples = ARCHIVE / "examples/source-based"
archived_examples.mkdir(parents=True, exist_ok=True)
for old_record in old_code_specs:
    path = example_dir / (old_record["page_id"] + ".py")
    target = archived_examples / path.name
    if path.exists() and not target.exists():
        shutil.copy2(path, target)
    assert target.read_text(encoding="utf-8").rstrip("\n") == old_record["code"]
active_examples = set()
for record in code_specs:
    name = record["page_id"] + ".py"
    active_examples.add(name)
    (example_dir / name).write_text(record["code"] + "\n", encoding="utf-8")
for path in example_dir.glob("*.py"):
    if path.name not in active_examples:
        assert path.resolve().is_relative_to(BOOK.resolve())
        assert digest(path.read_bytes()) == digest((archived_examples / path.name).read_bytes())
        path.unlink()

# Preserve the four original flow-vector records exactly; only screenshot IDs move.
assets = read_json("asset-manifest.json")
assert len(assets["items"]) == 34
image_uses = {}
for page in current_pages:
    for line in re.findall(r"^::image\{(.+)\}$", page, re.M):
        attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', line))
        image_uses.setdefault(attrs["src"], []).append({"page_id": page_id(page), **attrs})
# Root owns the new opening illustration and appends its manifest entry after
# this transformation; preserve that directive while validating retained assets.
summary_uses = image_uses.pop("assets/ch01/ai-human-summary.png", [])
assert not summary_uses or [use["page_id"] for use in summary_uses] == ["ch01-opening"]
active_items = []
for old_item in assets["items"]:
    if old_item["src"] == REMOVED_ASSET:
        path = BOOK / REMOVED_ASSET
        target = ARCHIVE / REMOVED_ASSET
        assert path.resolve().is_relative_to(BOOK.resolve())
        assert target.resolve().is_relative_to(ARCHIVE.resolve())
        target.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            if not target.exists():
                shutil.copy2(path, target)
            assert digest(path.read_bytes()) == digest(target.read_bytes())
            path.unlink()
        assert target.is_file()
        continue
    item = deepcopy(old_item)
    if item["src"] in image_uses:
        uses = image_uses[item["src"]]
        item["used_in"] = [use["page_id"] for use in uses]
        item["chapter"] = int(uses[0]["page_id"][2:4])
        item["placements"] = [{"page_id": use["page_id"], "width": use.get("width", "text"), "caption": use.get("caption", "")} for use in uses]
        item["placement_width"] = uses[0].get("width", "text")
        if "page_id" in item:
            item["page_id"] = mapping[item["page_id"]]
    else:
        assert item["kind"] == "user-supplied-pdf-native-vector-crop", item["src"]
        assert item == old_item
    assert (BOOK / item["src"]).is_file()
    assert digest((BOOK / item["src"]).read_bytes()) == item["sha256"]
    if item.get("vector_src"):
        assert digest((BOOK / item["vector_src"]).read_bytes()) == item["vector_sha256"]
    active_items.append(item)
assert len(active_items) == 33
assert len(image_uses) == 29 and sum(map(len, image_uses.values())) == 30
assets["items"] = active_items
assets["edition"] = EDITION
save_json("asset-manifest.json", assets)

source_map = read_json("source-map.json")
old_source_map = {record["chapter"]: record for record in source_map}
new_source_map = []
inverse_chapter_map = {new: old for old, new in CHAPTER_MAP.items()}
for number in range(1, 17):
    record = deepcopy(old_source_map[inverse_chapter_map.get(number, number)])
    record["chapter"] = number
    record["title"] = re.search(r"^# (.+)$", by_id[f"ch{number:02d}-opening"], re.M)[1]
    if number == 14:
        record["source_pages"] = "106-110, 118-127"
    new_source_map.append(record)
save_json("source-map.json", new_source_map)

previous_restructure = read_json("page-restructure.json")
composed = {old_id: (mapping[value] if value is not None else None) for old_id, value in previous_restructure["old_to_new"].items()}
previous_restructure["old_to_new"] = composed
previous_restructure["removed_pages"] = [key for key, value in composed.items() if value is None]
previous_restructure["added_pages"] = [mapping[value] for value in previous_restructure["added_pages"] if mapping[value] is not None]
previous_restructure.update({
    "date": "2026-10-11", "edition": EDITION,
    "expected_containers": 167, "expected_practices": 40,
    "expected_images": 35, "expected_assets": 34,
    "expected_code_blocks": 12, "expected_flowcharts": 4,
    "graph_first_restructure": "graph-first-restructure.json",
    "pending_root_asset": "assets/ch01/ai-human-summary.png",
})
assert len(previous_restructure["removed_pages"]) == 14
assert previous_restructure["added_pages"] == ["ch13-check", "ch14-opening"]
assert {value for value in composed.values() if value is not None} | set(previous_restructure["added_pages"]) == expected_ids
save_json("page-restructure.json", previous_restructure)

old_code_by_id = {record["page_id"]: record for record in old_code_specs}
result_by_id = {record["page_id"]: record for record in code_results["records"]}
for old_id, record in old_code_by_id.items():
    new_id = mapping[old_id]
    new_record = next(item for item in code_specs if item["page_id"] == new_id)
    assert new_record["code"] == record["code"] and new_record["output"] == record["output"]
    assert digest(new_record["code"].encode()) == result_by_id[new_id]["code_sha256"]
    assert (example_dir / (new_id + ".py")).read_text(encoding="utf-8").rstrip("\n") == record["code"]
old_hashes = Counter(record["code_sha256"] for record in old_code_results["records"])
assert old_hashes == Counter(record["code_sha256"] for record in code_results["records"])
old_flow = [value for text in old_chapters.values() for value in re.findall(r"```flowchart\s*\n(.*?)\n```", text, re.S)]
new_flow = [value for page in current_pages for value in re.findall(r"```flowchart\s*\n(.*?)\n```", page, re.S)]
assert len(old_flow) == len(new_flow) == 4 and old_flow == new_flow
old_outputs = [value for text in old_chapters.values() for value in re.findall(r"```output\s*\n(.*?)\n```", text, re.S)]
new_outputs = [value for page in current_pages for value in re.findall(r"```output\s*\n(.*?)\n```", page, re.S)]
assert len(old_outputs) == len(new_outputs) == 5 and old_outputs == new_outputs

save_json("graph-first-restructure.json", {
    "date": "2026-10-11", "edition": EDITION,
    "baseline": "previous-reports/20261011-before-graph-first",
    "old_to_new": mapping, "id_mapping": mapping,
    "removed_pages": sorted(REMOVED), "added_pages": [],
    "removed_assets": [REMOVED_ASSET],
    "chapter_mapping": {str(old): new for old, new in CHAPTER_MAP.items()},
    "previous_containers": 170, "expected_containers": 167,
    "previous_practices": 41, "expected_practices": 40,
    "expected_code_blocks": 12, "expected_flowcharts": 4,
    "base_retained_assets": 33, "base_retained_images": 34,
    "expected_assets_after_summary": 34, "expected_images_after_summary": 35,
    "summary_asset_added_by_root": "assets/ch01/ai-human-summary.png",
    "code_hashes_unchanged": True, "output_fences_unchanged": True,
    "flowchart_fences_unchanged": True,
    "practice_counts": {str(number): counts[number] for number in range(1, 17)},
})
print(json.dumps({
    "chapter_containers": 166, "assembled_containers": 167,
    "practices": 40, "codes": 12, "outputs": 5, "flowcharts": 4,
    "base_assets": 33, "base_image_placements": 34,
    "api_mentions": 0, "code_hashes_unchanged": True,
    "chapter_mapping": CHAPTER_MAP,
}, ensure_ascii=False))
