const projectPath = input?.file ?? dv.current().file.path;
const projectBase = projectPath.replace(/\.md$/, "");
const linksToProject = (task) =>
  task.text.includes(`[[${projectBase}]]`) || task.text.includes(`[[${projectBase}|`);

const tasks = dv
  .pages('""')
  .file
  .tasks.where((t) => t.completed)
  .where((t) => t.text.includes("#task"))
  .where((t) => t.path === projectPath || linksToProject(t))
  .sort((t) => t.completion?.toMillis() ?? 0, "desc");

dv.taskList(tasks, false);
