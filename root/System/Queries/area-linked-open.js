await dv.view("System/Queries/project-linked-open", {
  file: input?.file ?? dv.current().file.path
});
