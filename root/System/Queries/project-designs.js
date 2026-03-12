const projectPath = input?.file ?? dv.current().file.path;
const projectBase = projectPath.replace(/\.md$/, "");
const designsPrefix = `${projectBase}/designs/`;

const pages = dv
  .pages('""')
  .where((page) => page.file.path.startsWith(designsPrefix))
  .sort((page) => page.file.name, "asc");

if (!pages.length) {
  dv.paragraph("No project-owned design notes found.");
} else {
  dv.table(
    ["Design", "Source", "Role", "Google Doc"],
    pages.map((page) => [
      page.file.link,
      page.gdoc_source_of_truth ?? "",
      page.gdoc_role ?? "",
      page.gdoc_url ?? ""
    ])
  );
}
