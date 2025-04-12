import os
import caldav
from caldav.elements import dav, cdav
import datetime
import logging

APPLE_ID = os.getenv('APPLE_ID')
APPLE_PASSWORD = os.getenv('APPLE_PASSWORD')
CALENDAR_URL = 'https://caldav.icloud.com'  # We'll use the base URL

def get_caldav_client():
    return caldav.DAVClient(url=CALENDAR_URL, username=APPLE_ID, password=APPLE_PASSWORD)

def discover_caldav_calendars():
    try:
        client = get_caldav_client()
        principal = client.principal()
        logging.debug(f"Principal URL: {principal.url}")

        calendars = principal.calendars()

        if calendars:
            logging.debug("Available calendars:")
            for calendar in calendars:
                logging.debug(f"- {calendar.name} (URL: {calendar.url})")
        else:
            logging.debug("No calendars found.")

        return CALENDAR_URL

    except caldav.lib.error.AuthorizationError as e:
        logging.debug(f"Authorization failed: {e}")
    except Exception as e:
        logging.debug(f"An error occurred: {e}")

    return None

def get_apple_calendar_events(calendar_name, start_date, end_date):
    client = get_caldav_client()
    principal = client.principal()
    calendars = principal.calendars()

    calendar = next((cal for cal in calendars if cal.name == calendar_name), None)

    if calendar:
        events = calendar.search(start=start_date, end=end_date, event=True, expand=True)
        return events
    else:
        logging.debug(f"Calendar '{calendar_name}' not found.")
        return None

# def get_apple_calendar_todos(calendar_name, start_date, end_date):
#     client = get_caldav_client()
#     principal = client.principal()
#     calendars = principal.calendars()

#     calendar = next((cal for cal in calendars if cal.name == calendar_name), None)

#     acceptable_component_types = calendar.get_supported_components()
#     logging.debug(f"Supported component types: {acceptable_component_types}")

#     if calendar:
#         if "VTODO" in acceptable_component_types:
#             todos = calendar.search(start=start_date, end=end_date, todo=True, expand=True)
#             return todos
#         else:
#             logging.debug("VTODO component is not supported.")
#             return None
#     else:
#         logging.debug(f"Calendar '{calendar_name}' not found.")
#         return None

def add_event_to_calendar(calendar_name, summary, start_time, end_time):
    client = get_caldav_client()
    principal = client.principal()
    calendars = principal.calendars()

    calendar = next((cal for cal in calendars if cal.name == calendar_name), None)

    if calendar:
        event = calendar.save_event(
            dtstart=start_time,
            dtend=end_time,
            summary=summary
        )
        return True
    else:
        logging.debug(f"Calendar '{calendar_name}' not found.")
        return False

def update_event_in_calendar(calendar_name, event_uid, summary, start_time, end_time):
    client = get_caldav_client()
    principal = client.principal()
    calendars = principal.calendars()

    calendar = next((cal for cal in calendars if cal.name == calendar_name), None)

    if calendar:
        event = calendar.event(event_uid)
        event.load()
        event.instance.vevent.summary.value = summary
        event.instance.vevent.dtstart.value = start_time
        event.instance.vevent.dtend.value = end_time
        event.save()
        return True
    else:
        logging.debug(f"Calendar '{calendar_name}' not found.")
        return False

def delete_event_from_calendar(calendar_name, event_uid):
    client = get_caldav_client()
    principal = client.principal()
    calendars = principal.calendars()

    calendar = next((cal for cal in calendars if cal.name == calendar_name), None)

    if calendar:
        event = calendar.event(event_uid)
        event.delete()
        return True
    else:
        logging.debug(f"Calendar '{calendar_name}' not found.")
        return False

def list_calendars():
    client = get_caldav_client()
    principal = client.principal()
    calendars = principal.calendars()

    return [{'name': cal.name, 'url': cal.url} for cal in calendars]

# # Example usage
# if __name__ == "__main__":
#     caldav_url = discover_caldav_calendars()
#     if caldav_url:
#         logging.debug(f"\niCloud CalDAV is accessible. Base URL: {caldav_url}")

#         # List calendars
#         calendars = list_calendars()
#         logging.debug("\nCalendars:")
#         for cal in calendars:
#             logging.debug(f"- {cal['name']} ({cal['url']})")

#         # Example: Get events for a specific calendar
#         calendar_name = "calendar_name"
#         start_date = datetime.datetime.now()
#         end_date = start_date + datetime.timedelta(days=7)
#         events = get_apple_calendar_events(calendar_name, start_date, end_date)
#         if events:
#             logging.debug(f"\nEvents in '{calendar_name}' for the next 7 days:")
#             for event in events:
#                 logging.debug(f"- {event.instance.vevent.summary.value}")

#         # Example: Add an event
#         add_event_to_calendar(calendar_name, "[Testing] New Event", start_date, end_date)

#         # Note: For update and delete operations, you'd need the event's UID,
#         # which you can get from the event objects returned by get_apple_calendar_events
#     else:
#         logging.debug("\nFailed to access iCloud CalDAV.")