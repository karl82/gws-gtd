const canonicalProjectPattern = /^Projects\/[^/]+\/[^/]+\.md$/;
const canonicalDesignPattern = /^Projects\/[^/]+\/[^/]+\/designs\/[^/]+\.md$/;
const taskTagPattern = /(^|\s)#task(?=\s|$)/;
const inboxTagPattern = /(^|\s)#inbox(?=\s|$)/;
const fullProjectLinkPattern = /\[\[Projects\/[^\]|]+(?:\|[^\]]+)?\]\]/;
const fullAreaLinkPattern = /\[\[Areas\/[^\]|]+(?:\|[^\]]+)?\]\]/;
const wikiLinkPattern = /\[\[([^\]|]+)(?:\|[^\]]+)?\]\]/g;

const allPages = dv.pages('""');

const basenameMap = new Map();

const addCanonicalBasename = (page) => {
  const path = page.file.path.replace(/\.md$/, "");
  const name = path.split("/").pop();
  const existing = basenameMap.get(name) ?? [];
  existing.push(path);
  basenameMap.set(name, existing);
};

allPages
  .where(
    (page) =>
      page.file.path.startsWith("Projects/") ||
      page.file.path.startsWith("Areas/") ||
      page.file.path.startsWith("People/")
  )
  .forEach(addCanonicalBasename);

const extractWikiLinks = (text) => {
  const links = [];
  for (const match of text.matchAll(wikiLinkPattern)) {
    links.push(match[1]);
  }
  return links;
};

const hasShortCanonicalLink = (text) =>
  extractWikiLinks(text).some((link) => !link.includes("/") && basenameMap.has(link));

const normalizeLinkValue = (value) => {
  if (!value) {
    return "";
  }
  if (typeof value === "string") {
    return value;
  }
  if (typeof value.path === "string") {
    return value.path.replace(/\.md$/, "");
  }
  return "";
};

const renderSection = (title, rows, headers) => {
  dv.header(3, title);
  if (!rows.length) {
    dv.paragraph("None.");
    return;
  }
  dv.table(headers, rows);
};

const taskRows = dv
  .pages('""')
  .file
  .tasks.where((task) => taskTagPattern.test(task.text))
  .where((task) => !task.completed)
  .where((task) => !inboxTagPattern.test(task.text));

const projectTasksMissingFullLink = taskRows
  .where((task) => task.path.startsWith("Projects/"))
  .where((task) => !fullProjectLinkPattern.test(task.text))
  .map((task) => [dv.fileLink(task.path), task.text]);

const areaTasksMissingFullLink = taskRows
  .where((task) => task.path.startsWith("Areas/"))
  .where((task) => !fullAreaLinkPattern.test(task.text))
  .map((task) => [dv.fileLink(task.path), task.text]);

const tasksUsingShortCanonicalLinks = taskRows
  .where((task) => hasShortCanonicalLink(task.text))
  .map((task) => [dv.fileLink(task.path), task.text]);

const adaptableLegacyDesigns = allPages
  .where((page) => page.file.path.startsWith("Designs/"))
  .map((page) => [page.file.link, "Legacy top-level Designs/ note"]);

const likelyDesignPages = allPages.where(
  (page) =>
    page.file.path.startsWith("Designs/") ||
    page.file.path.includes("/designs/") ||
    page.project ||
    page.gdoc_id ||
    page.gdoc_url ||
    page.gdoc_source_of_truth
);

const designNotesOutsideCanonicalFolder = likelyDesignPages
  .where((page) => !canonicalDesignPattern.test(page.file.path))
  .where((page) => !page.file.path.startsWith("Designs/"))
  .where((page) => !page.file.path.startsWith("Resources/"))
  .map((page) => [page.file.link, page.file.path]);

const designNotesMissingProject = likelyDesignPages
  .where((page) => !page.file.path.startsWith("Resources/"))
  .where((page) => !normalizeLinkValue(page.project).startsWith("Projects/"))
  .map((page) => [page.file.link, page.project ?? ""]);

const designNotesMissingGdocFields = likelyDesignPages
  .where((page) => !page.file.path.startsWith("Resources/"))
  .where((page) => !page.gdoc_id || !page.gdoc_url || !page.gdoc_source_of_truth)
  .map((page) => [
    page.file.link,
    page.gdoc_id ?? "",
    page.gdoc_url ?? "",
    page.gdoc_source_of_truth ?? ""
  ]);

const tabBundlesMissingMetadata = likelyDesignPages
  .where((page) => page.gdoc_role || page.gdoc_tab_title)
  .where((page) => !(page.gdoc_role && page.gdoc_tab_title))
  .map((page) => [page.file.link, page.gdoc_role ?? "", page.gdoc_tab_title ?? ""]);

const projectNotesOutsideCanonicalPattern = allPages
  .where((page) => page.file.path.startsWith("Projects/"))
  .where((page) => !canonicalProjectPattern.test(page.file.path))
  .where((page) => !page.file.path.startsWith("Designs/"))
  .where((page) => !page.file.path.includes("/designs/"))
  .where((page) => !/^Projects\/[^/]+\/[^/]+\//.test(page.file.path))
  .map((page) => [page.file.link, page.file.path]);

renderSection("Project Tasks Missing Full Project Links", projectTasksMissingFullLink, ["Note", "Task"]);
renderSection("Area Tasks Missing Full Area Links", areaTasksMissingFullLink, ["Note", "Task"]);
renderSection("Tasks Using Short Canonical Links", tasksUsingShortCanonicalLinks, ["Note", "Task"]);
renderSection("Project Notes Outside Canonical Pattern", projectNotesOutsideCanonicalPattern, ["Note", "Path"]);
renderSection("Legacy Design Notes", adaptableLegacyDesigns, ["Note", "Classification"]);
renderSection("Design Notes Outside Project-Owned Folders", designNotesOutsideCanonicalFolder, ["Note", "Path"]);
renderSection("Design Notes Missing Project Link", designNotesMissingProject, ["Note", "Project"]);
renderSection("Design Notes Missing Google Doc Metadata", designNotesMissingGdocFields, ["Note", "gdoc_id", "gdoc_url", "gdoc_source_of_truth"]);
renderSection("Tabbed Review Notes Missing Tab Metadata", tabBundlesMissingMetadata, ["Note", "gdoc_role", "gdoc_tab_title"]);
