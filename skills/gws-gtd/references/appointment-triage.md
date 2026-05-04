# Appointment Triage

## Scope

- Apply this procedure when an email is a service/reservation/appointment confirmation or reschedule notification.
- Invoked from `gmail-intake.md § Step 1` when the classifier returns outcome `appointment`.
- Applies only to reservation/service-confirmation emails. Do not use this for generic meeting invites (those follow `calendar-intake.md`) or for email that is merely date-adjacent.
- The output of this procedure is a calendar event plus an archived email. No vault `#task` is created when the calendar already reflects (or will reflect) the appointment.

## Appointment Workflow

1. Search Google Calendar for an existing event matching the appointment (search by venue name, service type, or date range).
2. If an existing event is found:
   - Compare the email's date/time against the calendar event.
   - If they match: archive the email, no task needed.
   - If they differ (reschedule): patch the calendar event with the new date/time, then archive the email.
3. If no existing event is found:
   - Create a calendar event with `gws calendar +insert` using the appointment date/time, summary, and location from the email.
   - Archive the email after creation.
4. Never create a vault `#task` for an appointment that is already reflected (or can be reflected) in the calendar.
