import { Alert, Button, MultilineInput, Rows, Text } from "@canva/app-ui-kit";
import { openDesign } from "@canva/design";
import type { DesignEditing, RichtextRange } from "@canva/design";
import { useState } from "react";

type NativeText = { path: string; range: RichtextRange };

function textFields(page: DesignEditing.AbsolutePage): NativeText[] {
  const fields: NativeText[] = [];
  page.elements.toArray().forEach((element, index) => {
    if (element.type === "text") {
      fields.push({ path: String(index), range: element.text });
    } else if (element.type === "group") {
      element.contents.toArray().forEach((child, childIndex) => {
        if (child.type === "text") {
          fields.push({ path: `${index}.${childIndex}`, range: child.text });
        }
      });
    }
  });
  return fields;
}

/** Native pages are duplicated in Canva; this panel changes their text only. */
export function NativeTemplatePanel() {
  const [inventory, setInventory] = useState("");
  const [changes, setChanges] = useState("");
  const [pageId, setPageId] = useState<string>();
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);
  const [allPages, setAllPages] = useState(false);
  const [allPageIds, setAllPageIds] = useState<string[]>([]);

  const inspectAll = async () => {
    setBusy(true);
    try {
      await openDesign({ type: "all_pages" }, async (session) => {
        const pages: object[] = [];
        const ids: string[] = [];
        for (const ref of session.pageRefs.toArray()) {
          if (ref.type !== "absolute")
            throw new Error("고정 크기 페이지가 필요합니다.");
          const opened = await session.helpers.openPage(
            ref,
            async ({ page }) => {
              ids.push(page.id);
              pages.push({
                pageId: page.id,
                dimensions: page.dimensions,
                fields: textFields(page).map(({ path, range }) => ({
                  path,
                  text: range.readPlaintext(),
                })),
              });
            },
          );
          if (opened.status !== "executed")
            throw new Error("읽지 못한 페이지가 있습니다.");
        }
        setAllPages(true);
        setAllPageIds(ids);
        setPageId("all");
        setInventory(JSON.stringify(pages, null, 2));
        setMessage(`원본 틀 ${pages.length}페이지의 문구를 읽었습니다.`);
      });
    } catch (error) {
      setMessage(error instanceof Error ? error.message : String(error));
    } finally {
      setBusy(false);
    }
  };

  const inspect = async () => {
    setBusy(true);
    try {
      await openDesign({ type: "current_page" }, async ({ page }) => {
        if (page.type !== "absolute")
          throw new Error("고정 크기 페이지를 선택하세요.");
        setPageId(page.id);
        setAllPages(false);
        setInventory(
          JSON.stringify(
            {
              pageId: page.id,
              dimensions: page.dimensions,
              fields: textFields(page).map(({ path, range }) => ({
                path,
                text: range.readPlaintext(),
                regions: range.readTextRegions(),
              })),
            },
            null,
            2,
          ),
        );
        setMessage("현재 페이지의 문구를 읽었습니다.");
      });
    } catch (error) {
      setMessage(error instanceof Error ? error.message : String(error));
    } finally {
      setBusy(false);
    }
  };

  const apply = async () => {
    setBusy(true);
    try {
      const replacements: {
        pageId?: string;
        path: string;
        from: string;
        to: string;
      }[] = JSON.parse(changes);
      if (
        !Array.isArray(replacements) ||
        replacements.length === 0 ||
        replacements.some(
          (item) =>
            typeof item.path !== "string" ||
            typeof item.from !== "string" ||
            typeof item.to !== "string",
        )
      )
        throw new Error("문구 교체 목록을 확인하세요.");
      if (
        new Set(replacements.map((item) => `${item.pageId ?? ""}/${item.path}`))
          .size !== replacements.length
      )
        throw new Error("같은 문구 칸을 두 번 교체할 수 없습니다.");
      if (allPages) {
        if (
          replacements.some(
            (item) => !item.pageId || !allPageIds.includes(item.pageId),
          )
        )
          throw new Error("읽어 둔 페이지의 문구만 교체할 수 있습니다.");
        await openDesign({ type: "all_pages" }, async (session) => {
          if (session.pageRefs.toArray().length !== allPageIds.length)
            throw new Error(
              "페이지 구성이 바뀌었습니다. 모든 틀을 다시 읽으세요.",
            );
          const targets: { range: RichtextRange; from: string; to: string }[] =
            [];
          for (const [index, ref] of session.pageRefs.toArray().entries()) {
            if (ref.type !== "absolute")
              throw new Error("고정 크기 페이지가 필요합니다.");
            const opened = await session.helpers.openPage(
              ref,
              async ({ page }) => {
                if (page.id !== allPageIds[index])
                  throw new Error("페이지 순서가 바뀌었습니다.");
                const fields = textFields(page);
                for (const replacement of replacements.filter(
                  (item) => item.pageId === page.id,
                )) {
                  const field = fields.find(
                    (item) => item.path === replacement.path,
                  );
                  if (
                    !field ||
                    field.range.readPlaintext() !== replacement.from
                  )
                    throw new Error(
                      "원래 문구가 달라졌습니다. 모든 틀을 다시 읽으세요.",
                    );
                  targets.push({
                    range: field.range,
                    from: replacement.from,
                    to: replacement.to,
                  });
                }
              },
            );
            if (opened.status !== "executed")
              throw new Error("읽지 못한 페이지가 있습니다.");
          }
          // openPage snapshots its draft when the callback returns. Apply edits
          // inside that callback rather than holding ranges from a closed page.
          for (const [index, ref] of session.pageRefs.toArray().entries()) {
            const changesForPage = replacements.filter(
              (item) => item.pageId === allPageIds[index],
            );
            if (changesForPage.length === 0) continue;
            if (ref.type !== "absolute")
              throw new Error("고정 크기 페이지가 필요합니다.");
            const opened = await session.helpers.openPage(
              ref,
              async ({ page }) => {
                const fields = textFields(page);
                for (const replacement of changesForPage) {
                  const field = fields.find(
                    (item) => item.path === replacement.path,
                  );
                  if (
                    !field ||
                    field.range.readPlaintext() !== replacement.from
                  )
                    throw new Error("교체 직전에 원래 문구가 달라졌습니다.");
                  field.range.replaceText(
                    { index: 0, length: replacement.from.length },
                    replacement.to,
                  );
                }
              },
            );
            if (opened.status !== "executed")
              throw new Error("수정하지 못한 페이지가 있습니다.");
          }
          await session.sync();
          setMessage(
            `원본 틀을 유지하고 문구 ${targets.length}개를 교체했습니다.`,
          );
        });
        return;
      }
      await openDesign({ type: "current_page" }, async (session) => {
        if (session.page.type !== "absolute" || session.page.id !== pageId)
          throw new Error("페이지가 바뀌었습니다. 현재 틀을 다시 읽으세요.");
        const fields = textFields(session.page);
        const targets = replacements.map((replacement) => {
          const field = fields.find(
            (candidate) => candidate.path === replacement.path,
          );
          if (!field || field.range.readPlaintext() !== replacement.from)
            throw new Error(
              "원래 문구가 달라졌습니다. 현재 틀을 다시 읽으세요.",
            );
          return { field, replacement };
        });
        targets.forEach(({ field, replacement }) => {
          field.range.replaceText(
            { index: 0, length: replacement.from.length },
            replacement.to,
          );
        });
        await session.sync();
        setMessage(
          `원본 틀을 유지하고 문구 ${targets.length}개를 교체했습니다.`,
        );
      });
    } catch (error) {
      setMessage(error instanceof Error ? error.message : String(error));
    } finally {
      setBusy(false);
    }
  };

  return (
    <Rows spacing="1u">
      <Text variant="bold">복제한 원본 틀의 문구 교체</Text>
      <Text size="small">
        Canva에서 복제한 페이지를 선택하세요. 문구 교체 전후에 배치와 줄바꿈을
        확인하세요.
      </Text>
      <Button
        variant="secondary"
        disabled={busy}
        onClick={() => void inspect()}
      >
        현재 틀 읽기
      </Button>
      <Button
        variant="secondary"
        disabled={busy}
        onClick={() => void inspectAll()}
      >
        모든 틀 읽기
      </Button>
      <MultilineInput
        placeholder="현재 틀의 문구"
        value={inventory}
        onChange={setInventory}
        minRows={3}
      />
      <MultilineInput
        placeholder="문구 교체 목록 (path, from, to)"
        value={changes}
        onChange={setChanges}
        minRows={3}
      />
      <Button
        variant="secondary"
        disabled={busy || !pageId || !changes.trim()}
        onClick={() => void apply()}
      >
        선택한 틀의 문구 교체
      </Button>
      {message && <Alert tone="info">{message}</Alert>}
    </Rows>
  );
}
