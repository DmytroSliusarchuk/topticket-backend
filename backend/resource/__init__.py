from backend.resource.auth import register, login
from backend.resource.users import get_user_by_username, get_user_by_id, delete_user_by_id, update_user_by_username
from backend.resource.events import create_event, get_event_by_id, delete_event_by_id, update_event, get_all_events
from backend.resource.tickets import create_ticket, get_ticket_by_id, get_all_tickets_by_eventid, \
    get_all_tickets_by_userid, update_ticket, delete_ticket_by_id, buy_ticket, book_ticket, cancel_book_ticket
