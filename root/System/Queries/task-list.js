const notePath = input?.file ?? dv.current().file.path;
const preset = input?.preset ?? "next-no-due";

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

const tagPattern = (tag) => new RegExp(`(^|\\s)#${tag}(?=\\s|$)`);
const hasTaskTag = (task) => tagPattern("task").test(task.text);
const hasInboxTag = (task) => tagPattern("inbox").test(task.text);
const hasNextTag = (task) => tagPattern("next").test(task.text);
const hasWaitingTag = (task) => tagPattern("waiting").test(task.text);
const hasSomedayTag = (task) => tagPattern("someday").test(task.text);
const toMillis = (dt) => dt?.toMillis?.() ?? Number.MAX_SAFE_INTEGER;
const inlineMetadataPattern = /\s*(?:\[[^\]]+::[^\]]*\]|\([^()]*::[^()]*\))/g;
const areaOrProjectLinkPattern = /\[\[(Projects|Areas)\/[^\]|]+(?:\|[^\]]+)?\]\]/;
const canonicalProjectPathPattern = /^Projects\/[^/]+\/[^/]+\.md$/;

const isExecutionPath = (path) => path.startsWith("Projects/") || path.startsWith("Areas/");

const projectLinkBase = (path) => path.replace(/\.md$/, "");

const isTaskLinkedToProject = (task, projectPath) => {
  const base = projectLinkBase(projectPath);
  return task.path === projectPath || task.text.includes(`[[${base}]]`) || task.text.includes(`[[${base}|`);
};

const hasAreaOrProjectLink = (task) => areaOrProjectLinkPattern.test(task.text);

const normalizeSpaces = (text) => text.replace(/\s{2,}/g, " ").trim();

const taskVisual = (task) => {
  const withoutMetadata = normalizeSpaces(task.text.replace(inlineMetadataPattern, ""));
  const subject = typeof task.subject === "string" ? task.subject.trim() : "";
  if (!subject || withoutMetadata.includes(subject)) {
    return withoutMetadata;
  }
  return `${withoutMetadata} *${subject}*`;
};

const renderTaskList = (tasks) => {
  const prepared = tasks.map((task) => {
    task.visual = taskVisual(task);
    return task;
  });
  dv.taskList(prepared, false);
};

const allTasks = dv
  .pages('""')
  .file
  .tasks.where((task) => !isExcludedPath(task.path))
  .where((task) => hasTaskTag(task));

const sortByDue = (tasks) => tasks.sort((task) => toMillis(task.due), "asc");

if (preset === "inbox") {
  const tasks = sortByDue(allTasks.where((task) => !task.completed && hasInboxTag(task)));
  renderTaskList(tasks);
  return;
}

if (preset === "next-explicit") {
  const tasks = allTasks
    .where((task) => !task.completed)
    .where((task) => !hasInboxTag(task))
    .where((task) => hasNextTag(task))
    .sort((task) => task.text, "asc");
  renderTaskList(tasks);
  return;
}

if (preset === "next-candidates") {
  const tasks = allTasks
    .where((task) => !task.completed)
    .where((task) => !hasInboxTag(task))
    .where((task) => !hasNextTag(task))
    .where((task) => !hasWaitingTag(task))
    .where((task) => !hasSomedayTag(task))
    .sort((task) => task.path, "asc");
  renderTaskList(tasks);
  return;
}

if (preset === "due-7") {
  const dueBy = dv.date("today").plus({ days: 7 }).toMillis();
  const tasks = sortByDue(
    allTasks
      .where((task) => !task.completed)
      .where((task) => !hasInboxTag(task))
      .where((task) => task.due && toMillis(task.due) <= dueBy)
  );
  renderTaskList(tasks);
  return;
}

if (preset === "waiting") {
  const tasks = sortByDue(
    allTasks
      .where((task) => !task.completed)
      .where((task) => !hasInboxTag(task))
      .where((task) => hasWaitingTag(task))
  );
  renderTaskList(tasks);
  return;
}

if (preset === "overdue") {
  const today = dv.date("today").toMillis();
  const tasks = sortByDue(
    allTasks
      .where((task) => !task.completed)
      .where((task) => !hasInboxTag(task))
      .where((task) => task.due && toMillis(task.due) < today)
  );
  renderTaskList(tasks);
  return;
}

if (preset === "daily-due") {
  const noteName = notePath.split("/").pop().replace(/\.md$/, "");
  const parsed = window.moment(noteName, "YYYY-MM-DD", true);
  const target = parsed.isValid() ? parsed : window.moment();
  const tasks = sortByDue(
    allTasks
      .where((task) => !task.completed)
      .where((task) => !hasInboxTag(task))
      .where((task) => task.due)
      .where((task) => window.moment(task.due.toISODate()).isSame(target, "day"))
  );
  dv.header(3, `Tasks Due ${target.format("YYYY-MM-DD")}`);
  renderTaskList(tasks);
  return;
}

if (preset === "weekly-due") {
  const noteName = notePath.split("/").pop().replace(/\.md$/, "");
  const parsed = window.moment(noteName, "GGGG-[W]WW", true);
  const anchor = parsed.isValid() ? parsed : window.moment();
  const start = anchor.clone().startOf("isoWeek");
  const end = anchor.clone().endOf("isoWeek");
  const tasks = sortByDue(
    allTasks
      .where((task) => !task.completed)
      .where((task) => !hasInboxTag(task))
      .where((task) => task.due)
      .where((task) => {
        const due = window.moment(task.due.toISODate());
        return due.isSameOrAfter(start, "day") && due.isSameOrBefore(end, "day");
      })
  );
  dv.header(3, `Due This Week (${start.format("YYYY-MM-DD")} to ${end.format("YYYY-MM-DD")})`);
  renderTaskList(tasks);
  return;
}

if (preset === "monthly-due") {
  const noteName = notePath.split("/").pop().replace(/\.md$/, "");
  const parsed = window.moment(noteName, "YYYY-MM", true);
  const anchor = parsed.isValid() ? parsed : window.moment();
  const start = anchor.clone().startOf("month");
  const end = anchor.clone().endOf("month");
  const tasks = sortByDue(
    allTasks
      .where((task) => !task.completed)
      .where((task) => !hasInboxTag(task))
      .where((task) => task.due)
      .where((task) => {
        const due = window.moment(task.due.toISODate());
        return due.isSameOrAfter(start, "day") && due.isSameOrBefore(end, "day");
      })
  );
  dv.header(3, `Due This Month (${start.format("YYYY-MM-DD")} to ${end.format("YYYY-MM-DD")})`);
  renderTaskList(tasks);
  return;
}

if (preset === "project-health") {
  const openLinkedCount = (projectPath) =>
    allTasks
      .where((task) => !task.completed)
      .where((task) => !hasInboxTag(task))
      .where((task) => isTaskLinkedToProject(task, projectPath)).length;

  const projects = dv
    .pages('"Projects"')
    .where((page) => canonicalProjectPathPattern.test(page.file.path))
    .sort((page) => page.file.mtime, "asc");
  dv.table(
    ["Project", "Last Modified", "Open #task"],
    projects.map((page) => [
      page.file.link,
      page.file.mtime,
      openLinkedCount(page.file.path)
    ])
  );
  return;
}

if (preset === "areas-list") {
  const areas = dv.pages('"Areas"').sort((page) => page.file.name, "asc");
  dv.list(areas.map((page) => page.file.link));
  return;
}

if (preset === "stalled-14") {
  const stalledBefore = dv.date("today").minus({ days: 14 }).toMillis();
  const openLinkedCount = (projectPath) =>
    allTasks
      .where((task) => !task.completed)
      .where((task) => !hasInboxTag(task))
      .where((task) => isTaskLinkedToProject(task, projectPath)).length;

  const projects = dv
    .pages('"Projects"')
    .where((page) => canonicalProjectPathPattern.test(page.file.path))
    .where((page) => {
      const openCount = openLinkedCount(page.file.path);
      return toMillis(page.file.mtime) < stalledBefore || openCount === 0;
    })
    .sort((page) => page.file.mtime, "asc");

  dv.table(
    ["Project", "Last Modified", "Open #task"],
    projects.map((page) => [
      page.file.link,
      page.file.mtime,
      openLinkedCount(page.file.path)
    ])
  );
  return;
}

if (preset === "orphan-open") {
  const tasks = allTasks
    .where((task) => !task.completed)
    .where((task) => !hasInboxTag(task))
    .where((task) => !isExecutionPath(task.path))
    .where((task) => !hasAreaOrProjectLink(task))
    .sort((task) => task.path, "asc");

  renderTaskList(tasks);
  return;
}

if (preset === "stalled-30") {
  const stalledBefore = dv.date("today").minus({ days: 30 }).toMillis();
  const openLinkedCount = (projectPath) =>
    allTasks
      .where((task) => !task.completed)
      .where((task) => !hasInboxTag(task))
      .where((task) => isTaskLinkedToProject(task, projectPath)).length;

  const projects = dv
    .pages('"Projects"')
    .where((page) => canonicalProjectPathPattern.test(page.file.path))
    .where((page) => toMillis(page.file.mtime) < stalledBefore)
    .sort((page) => page.file.mtime, "asc");

  dv.table(
    ["Project", "Last Modified", "Open #task"],
    projects.map((page) => [
      page.file.link,
      page.file.mtime,
      openLinkedCount(page.file.path)
    ])
  );
  return;
}

dv.paragraph(`Unknown task-list preset: ${preset}`);
