const projectPath = input?.file ?? dv.current().file.path;
const projectBase = projectPath.replace(/\.md$/, "");
const linksToProject = (task) =>
  task.text.includes(`[[${projectBase}]]`) || task.text.includes(`[[${projectBase}|`);

const tasks = dv
  .pages('""')
  .file
  .tasks.where((t) => !t.completed)
  .where((t) => t.text.includes("#task"))
  .where((t) => !t.text.includes("#inbox"))
  .where((t) => t.path === projectPath || linksToProject(t))
  .sort((t) => t.due?.toMillis() ?? Number.MAX_SAFE_INTEGER, "asc");

dv.taskList(tasks, false);
