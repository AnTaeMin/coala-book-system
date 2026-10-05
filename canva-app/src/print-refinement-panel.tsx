import { Alert, Button, MultilineInput, Rows, Text, TextInput } from "@canva/app-ui-kit";
import { openDesign } from "@canva/design";
import type { DesignEditing } from "@canva/design";
import { useState } from "react";

function mediaSnapshot(media: DesignEditing.MediaFill | undefined) {
  if (!media) return undefined;
  return media.type === "image"
    ? { type: "image", imageRef: media.imageRef, flipX: media.flipX, flipY: media.flipY }
    : { type: "video", videoRef: media.videoRef, flipX: media.flipX, flipY: media.flipY };
}
function colorSnapshot(color: DesignEditing.ColorFill | undefined) {
  return color?.type === "solid" ? { type: "solid", color: color.color } : undefined;
}
function strokeSnapshot(stroke: DesignEditing.Stroke | undefined) {
  return stroke ? { weight: stroke.weight, colorContainer: colorSnapshot(stroke.colorContainer.ref) } : undefined;
}

function snapshot(element: DesignEditing.AbsoluteElement): object {
  const base = {
    type: element.type, left: element.left, top: element.top,
    width: element.width, height: element.height,
    locked: element.locked, rotation: element.rotation,
    transparency: element.transparency,
  };
  if (element.type === "text") return {
    ...base, text: element.text.readPlaintext(),
    regions: element.text.readTextRegions(),
  };
  if (element.type === "shape") return {
    ...base, viewBox: { left: element.viewBox.left, top: element.viewBox.top,
      width: element.viewBox.width, height: element.viewBox.height },
    paths: element.paths.toArray().map(path => ({
      d: path.d, fill: {
        isMediaEditable: path.fill.isMediaEditable,
        mediaContainer: mediaSnapshot(path.fill.mediaContainer.ref),
        colorContainer: colorSnapshot(path.fill.colorContainer.ref),
      }, stroke: strokeSnapshot(path.stroke),
    })),
  };
  if (element.type === "rect") return {
    ...base, fill: {
      mediaContainer: mediaSnapshot(element.fill.mediaContainer.ref),
      colorContainer: colorSnapshot(element.fill.colorContainer.ref),
    }, stroke: strokeSnapshot(element.stroke),
  };
  if (element.type === "group") return {
    ...base, contents: element.contents.toArray().map(snapshot),
  };
  return base;
}

type InsertSpec =
  | ({ type: "text" } & DesignEditing.CreateTextElementOpts)
  | ({ type: "shape" } & DesignEditing.CreateShapeElementOpts)
  | ({ type: "rect" } & DesignEditing.CreateRectElementOpts);

function buildState(builder: DesignEditing.ElementStateBuilder, state: InsertSpec) {
  if (state.type === "text") return builder.createTextElement(state);
  if (state.type === "shape") return builder.createShapeElement(state);
  return builder.createRectElement(state);
}

type PageChange = {
  pageId: string;
  pageNumber: number;
  designPageCount: number;
  expectedCount: number;
  remove?: number[];
  replace?: { index: number; state: InsertSpec; behind?: boolean }[];
  append?: InsertSpec[];
  move?: { index: number; top: number; left?: number }[];
  whiteBackground?: boolean;
};

/** Visible, reviewable SDK editing workflow for the user's production copy. */
export function PrintRefinementPanel() {
  const [inventory, setInventory] = useState("");
  const [plan, setPlan] = useState("");
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  const [ids, setIds] = useState<string[]>([]);
  const [firstPage, setFirstPage] = useState("1");
  const [lastPage, setLastPage] = useState("12");

  const inspect = async () => {
    setBusy(true);
    try {
      await openDesign({ type: "all_pages" }, async session => {
        const pages: object[] = [];
        const refs = session.pageRefs.toArray();
        const nextIds: string[] = Array.from({ length: refs.length }, (_, i) => ids[i] ?? "");
        for (const [index, ref] of refs.entries()) {
          if (index + 1 < Number(firstPage) || index + 1 > Number(lastPage)) continue;
          if (ref.type !== "absolute") throw new Error("고정 크기 지면이 필요합니다.");
          const result = await session.helpers.openPage(ref, async ({ page }) => {
            nextIds[index] = page.id;
            pages.push({ pageNumber: index + 1, pageId: page.id, dimensions: page.dimensions ? {
              width: page.dimensions.width, height: page.dimensions.height } : undefined,
              background: page.background ? {
                color: colorSnapshot(page.background.colorContainer.ref),
                media: mediaSnapshot(page.background.mediaContainer.ref),
              } : undefined,
              elements: page.elements.toArray().map(snapshot) });
          });
          if (result.status !== "executed") throw new Error("지면을 읽지 못했습니다.");
        }
        setIds(nextIds);
        setInventory(JSON.stringify(pages, null, 2));
        setMessage(`${pages.length}쪽의 실제 배치를 읽었습니다.`);
      });
    } catch (error) {
      setMessage(error instanceof Error ? error.message : String(error));
    } finally { setBusy(false); }
  };

  const apply = async () => {
    setBusy(true);
    try {
      const changes: PageChange[] = JSON.parse(plan);
      if (!Array.isArray(changes) || !changes.length ||
          new Set(changes.map(c => c.pageId)).size !== changes.length ||
          changes.some(c => !Number.isInteger(c.pageNumber) || c.pageNumber < 1 || c.pageNumber > c.designPageCount))
        throw new Error("읽어 둔 지면의 수정 계획을 입력하세요.");
      await openDesign({ type: "all_pages" }, async session => {
        const refs = session.pageRefs.toArray();
        if (changes.some(c => c.designPageCount !== refs.length)) throw new Error("지면을 다시 읽으세요.");
        // Validate every target before beginning the write pass.
        for (const [index, ref] of refs.entries()) {
          const change = changes.find(c => c.pageNumber === index + 1);
          if (!change) continue;
          if (ref.type !== "absolute") throw new Error("지원하지 않는 지면입니다.");
          await session.helpers.openPage(ref, async ({ page }) => {
            const elements = page.elements.toArray();
            if (page.id !== change.pageId || elements.length !== change.expectedCount)
              throw new Error("배치가 달라졌습니다. 지면을 다시 읽으세요.");
            const targets = [...(change.remove ?? []), ...(change.replace ?? []).map(c => c.index), ...(change.move ?? []).map(c => c.index)];
            if (new Set(targets).size !== targets.length ||
                targets.some(i => !Number.isInteger(i) || i < 0 || i >= elements.length))
              throw new Error("수정할 요소 번호를 확인하세요.");
          });
        }
        let applied = 0;
        for (const [index, ref] of refs.entries()) {
          const change = changes.find(c => c.pageNumber === index + 1);
          if (!change || ref.type !== "absolute") continue;
          const result = await session.helpers.openPage(ref, async ({ page, helpers }) => {
            const elements = page.elements.toArray();
            if (page.elements.count() !== change.expectedCount)
              throw new Error("교체 직전 지면이 바뀌었습니다.");
            for (const movement of change.move ?? []) {
              const element = elements[movement.index];
              if (!element || element.type === "unsupported" || element.locked)
                throw new Error("이동할 수 없는 요소입니다.");
              element.top = movement.top;
              if (movement.left !== undefined) element.left = movement.left;
            }
            if (change.whiteBackground && page.background) {
              page.background.mediaContainer.set(undefined);
              page.background.colorContainer.set({ type: "solid", color: "#ffffff" });
              for (const element of elements) {
                if (element.type !== "shape") continue;
                for (const path of element.paths.toArray()) {
                  const fill = path.fill.colorContainer.ref;
                  if (fill?.type === "solid" && fill.color.toLowerCase() === "#f8f9fa")
                    path.fill.colorContainer.set({ type: "solid", color: "#ffffff" });
                }
              }
            }
            for (const replacement of change.replace ?? []) {
              const element = elements[replacement.index];
              if (!element) throw new Error("교체할 요소가 없습니다.");
              page.elements.insertBefore(replacement.behind ? page.elements.toArray()[0] : element,
                buildState(helpers.elementStateBuilder, replacement.state));
              page.elements.delete(element);
            }
            for (const at of change.remove ?? []) {
              const element = elements[at];
              if (!element) throw new Error("제거할 요소가 없습니다.");
              page.elements.delete(element);
            }
            for (const state of change.append ?? [])
              page.elements.insertAfter(undefined, buildState(helpers.elementStateBuilder, state));
            applied += 1;
          });
          if (result.status !== "executed") throw new Error("수정하지 못한 지면이 있습니다.");
        }
        await session.sync();
        setMessage(`${applied}쪽의 지면 수정을 저장했습니다.`);
      });
    } catch (error) {
      setMessage(error instanceof Error ? error.message : String(error));
    } finally { setBusy(false); }
  };

  return <Rows spacing="1u">
    <Text variant="bold">교재 지면 다듬기</Text>
    <Text size="small">배치를 먼저 확인한 뒤 제작 사본의 배경·상자·활동 영역을 수정합니다.</Text>
    <TextInput placeholder="배치 확인 시작 쪽" value={firstPage} onChange={setFirstPage} disabled={busy} />
    <TextInput placeholder="배치 확인 마지막 쪽" value={lastPage} onChange={setLastPage} disabled={busy} />
    <Button variant="secondary" disabled={busy} onClick={() => void inspect()}>지면 배치 읽기</Button>
    <MultilineInput placeholder="지면 배치 확인 결과" minRows={3} value={inventory} onChange={setInventory} />
    <MultilineInput placeholder="지면 수정 계획" minRows={3} value={plan} onChange={setPlan} />
    <Button variant="secondary" disabled={busy || !plan.trim()} onClick={() => void apply()}>계획한 지면 수정</Button>
    {message && <Alert tone="info">{message}</Alert>}
  </Rows>;
}
