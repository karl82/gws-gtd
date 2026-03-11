await dv.view("System/Queries/task-list", {
  preset: "monthly-due",
  file: input?.file ?? dv.current().file.path
});
