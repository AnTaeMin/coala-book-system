import { layoutPage } from "../src/builder/create-page";
import type { PracticeOpeningPage } from "../src/types/book-spec";
import { PAGE } from "../src/theme/page-layout";
import {
  findText,
  installRecordingRichtext,
  wantedSansFonts,
} from "./helpers/richtext";

const page: PracticeOpeningPage = {
  type: "practice-opening",
  id: "practice-001-1",
  practiceId: "001-1",
  practiceKind: "AI와 대화",
  platform: "알고플로에서 실습하기",
  title: "AI는 어떤 질문을 잘하고, 어떤 질문을 어려워할까?",
  description:
    "생성형 AI는 다양한 질문에 답할 수 있지만, 모든 질문에 항상 정확하게 답할 수 있는 것은 아닙니다.\n\n이번 활동에서는 생성형 AI가 잘 답할 수 있는 질문과 어려워하는 질문을 직접 비교하며 AI의 특성과 한계를 이해해봅니다.",
  tip: "생성형 AI가 잘 수행한 질문과 그렇지 않은 질문을 구분해보세요.",
};

type Shape = { left: number; top: number; width: number; height: number };

/** 도형 요소의 상자만 뽑는다. SDK 타입은 좁히기 어려워 형태만 읽는다. */
const shapeBoxes = (elements: readonly { type: string }[]): Shape[] =>
  elements
    .filter((element) => element.type === "shape")
    .map((element) => element as unknown as Shape);

beforeEach(() => installRecordingRichtext());

describe("실습 오프닝 카드", () => {
  it("배지, 제목, 설명을 감싸는 흰 카드를 그린다", () => {
    const elements = layoutPage(page, wantedSansFonts)[0]?.elements ?? [];
    const shapes = shapeBoxes(elements);
    // 원본 practice-opening1.png: 카드 x 160, y 157, 폭 ≈1262.
    const card = shapes.find(
      (shape) => shape.top === 157 && shape.width > 1200 && shape.height > 400,
    );
    expect(card).toBeDefined();

    const title = findText(elements, page.title);
    const platform = findText(elements, "알고플로에서 실습하기");
    const lastLine = findText(
      elements,
      "이번 활동에서는 생성형 AI가 잘 답할 수 있는 질문과 어려워하는 질문을 직접 비교하며 AI의 특성과 한계를 이해해봅니다.",
    );
    // 모두 카드 안에 있어야 한다.
    for (const inside of [title, platform, lastLine]) {
      expect(inside.top).toBeGreaterThan(card?.top ?? 0);
      expect(inside.top).toBeLessThan((card?.top ?? 0) + (card?.height ?? 0));
      expect(inside.left).toBeGreaterThanOrEqual(card?.left ?? 0);
    }
    expect(title.fontSizePt).toBe(30);
    expect(lastLine.fontSizePt).toBe(28);
  });

  it("실습 플랫폼 배지는 카드 오른쪽 끝에 붙는다", () => {
    const elements = layoutPage(page, wantedSansFonts)[0]?.elements ?? [];
    const platform = findText(elements, "알고플로에서 실습하기");
    const practice = findText(elements, "실습 001-1");

    expect(platform.left).toBeGreaterThan(PAGE.width / 2);
    expect(platform.left + platform.width).toBeLessThanOrEqual(1427 - 58);
    expect(practice.left).toBe(160 + 58);
  });

  it("Tip 박스는 카드 아래에 온다", () => {
    const elements = layoutPage(page, wantedSansFonts)[0]?.elements ?? [];
    const tip = findText(elements, "💡  Tip");
    const card = shapeBoxes(elements).find(
      (shape) => shape.top === 157 && shape.width > 1200,
    );
    expect(tip.top).toBeGreaterThan((card?.top ?? 0) + (card?.height ?? 0));
  });

  it("자리가 있으면 Tip 아래에 실습 목표까지 같은 페이지에 놓는다", () => {
    const objectives = [
      "AI가 잘 답한 질문과 그렇지 않은 질문을 구분할 수 있다.",
      "질문 유형에 따라 AI의 응답이 어떻게 달라지는지 설명할 수 있다.",
    ];
    const parts = layoutPage({ ...page, objectives }, wantedSansFonts);
    expect(parts).toHaveLength(1);

    const elements = parts[0]?.elements ?? [];
    const tip = findText(elements, "💡  Tip");
    const heading = findText(elements, "📑 실습 목표");
    const first = findText(elements, objectives[0] ?? "");
    expect(heading.top).toBeGreaterThan(tip.top);
    expect(first.top).toBeGreaterThan(heading.top);
    expect(first.top).toBeLessThan(PAGE.safeBottom);
  });

  it("실습 목표만 있으면 카드 바로 아래에 놓는다", () => {
    const { tip: _tip, ...withoutTip } = page;
    const elements =
      layoutPage(
        { ...withoutTip, objectives: ["목표 하나를 이룰 수 있다."] },
        wantedSansFonts,
      )[0]?.elements ?? [];
    const card = shapeBoxes(elements).find(
      (shape) => shape.top === 157 && shape.width > 1200,
    );
    const heading = findText(elements, "📑 실습 목표");
    expect(heading.top).toBeGreaterThan((card?.top ?? 0) + (card?.height ?? 0));
    expect(elements.some((e) => (e as { text?: string }).text === "💡  Tip")).toBe(
      false,
    );
  });

  it("실습 목표가 들어가지 않으면 다음 페이지로 넘긴다", () => {
    const objectives = Array.from(
      { length: 14 },
      (_, index) =>
        `${index + 1}번째 목표입니다. 생성형 AI의 특성과 한계를 설명하고 질문 유형에 따라 응답이 어떻게 달라지는지 비교할 수 있다.`,
    );
    const parts = layoutPage({ ...page, objectives }, wantedSansFonts);
    expect(parts.length).toBeGreaterThan(1);
    expect(parts[1]?.title).toContain("(계속)");
  });
});
