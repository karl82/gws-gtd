const personPath = input?.file ?? dv.current().file.path;
const personPathNoExt = personPath.replace(/\.md$/, "");
const personName = personPathNoExt.split("/").pop();

const configPage = dv.page("System/Queries/Task Query Config");
const excludedPathPrefixes = Array.isArray(configPage?.excludedPathPrefixes)
  ? configPage.excludedPathPrefixes
  : ["System/Templates/", "Archive/"];
const excludedExactPaths = Array.isArray(configPage?.excludedExactPaths)
  ? configPage.excludedExactPaths
  : ["AGENTS.md", "README.md"];

const isExcludedPath = (path) =>
  excludedExactPaths.includes(path) ||
  excludedPathPrefixes.some((prefix) => path.startsWith(prefix));

const escapeRegex = (value) => value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
const mentionRegex = new RegExp(`\\[\\[(?:People/)?${escapeRegex(personName)}(?:\\|[^\\]]+)?\\]\\]`);
const taskLineRegex = /^\s*[-*+]\s*\[[ xX-]\]\s+/;

const hasPersonOutlink = (page) => {
  const outlinks = page.file.outlinks ?? [];
  return outlinks.some((link) => {
    const rawPath = typeof link === "string" ? link : link.path ?? "";
    const normalizedPath = rawPath.replace(/\.md$/, "");
    return (
      normalizedPath === personPathNoExt ||
      normalizedPath === `People/${personName}` ||
      normalizedPath === personName
    );
  });
};

const candidatePages = dv
  .pages('""')
  .where((page) => page.file.path !== personPath)
  .where((page) => !isExcludedPath(page.file.path))
  .where((page) => hasPersonOutlink(page));

const rows = [];

for (const page of candidatePages.array()) {
  const abstract = app.vault.getAbstractFileByPath(page.file.path);
  if (!abstract) {
    continue;
  }

  const content = await app.vault.cachedRead(abstract);
  const lines = content.split(/\r?\n/);
  let inCodeFence = false;

  lines.forEach((line, index) => {
    if (/^\s*```/.test(line)) {
      inCodeFence = !inCodeFence;
      return;
    }

    if (inCodeFence) {
      return;
    }

    if (!mentionRegex.test(line)) {
      return;
    }

    if (taskLineRegex.test(line) || line.includes("#task")) {
      return;
    }

    const text = line.trim();
    if (!text) {
      return;
    }

    rows.push({
      when: page.file.day ?? page.file.mtime,
      whenMillis: page.file.day?.toMillis?.() ?? page.file.mtime?.toMillis?.() ?? 0,
      file: page.file.link,
      line: index + 1,
      text
    });
  });
}

if (!rows.length) {
  dv.paragraph("No non-task mentions found.");
} else {
  rows.sort((a, b) => b.whenMillis - a.whenMillis || a.line - b.line);
  dv.table(
    ["When", "Note", "Line", "Mention"],
    rows.map((row) => [row.when, row.file, row.line, row.text])
  );
}
