await dv.view("System/Queries/task-list", {
  preset: "weekly-due",
  file: input?.file ?? dv.current().file.path
});
