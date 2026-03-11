<%*
const parsed = window.moment(tp.file.title, "YYYY-MM-DD", true);
const dailyDate = parsed.isValid() ? parsed.format("YYYY-MM-DD") : tp.date.now("YYYY-MM-DD");
-%>
# Daily - <% dailyDate %>

## Notes

- <% tp.file.cursor(1) %>
