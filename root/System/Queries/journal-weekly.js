const notePath = input?.file ?? dv.current().file.path;
const noteName = notePath.split("/").pop().replace(/\.md$/, "");
const parsed = window.moment(noteName, "GGGG-[W]WW", true);
const anchor = parsed.isValid() ? parsed : window.moment();
const start = anchor.clone().startOf("isoWeek");
const end = anchor.clone().endOf("isoWeek");

dv.header(3, `Journal Entries (${start.format("YYYY-MM-DD")} to ${end.format("YYYY-MM-DD")})`);
dv.table(
  ["Date", "File"],
  dv
    .pages('"Journal"')
    .where((p) => p.file.day)
    .where((p) => {
      const day = window.moment(p.file.day.toISODate());
      return day.isSameOrAfter(start, "day") && day.isSameOrBefore(end, "day");
    })
    .sort((p) => p.file.day, "asc")
    .map((p) => [p.file.day, p.file.link])
);
