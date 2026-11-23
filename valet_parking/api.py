import frappe

@frappe.whitelist(allow_guest=True)
def request_vehicle(ticket_id, phone_number):
    ticket_id = (ticket_id or "").strip()
    phone_number = (phone_number or "").strip()

    if not frappe.db.exists("Valet Ticket", ticket_id):
        return {"status": "error", "message": "Invalid Ticket ID. Please check your slip."}

    ticket = frappe.get_doc("Valet Ticket", ticket_id)
    if phone_number[-4:] not in (ticket.phone_number or ""):
        return {"status": "error", "message": "Phone number does not match this ticket."}

    if ticket.status == "Completed":
        return {"status": "error", "message": "This vehicle has already been checked out."}

    ticket.db_set("status", "Requested")
    return {
        "status": "success",
        "message": f"Car ({ticket.vehicle_plate_number}) requested! Please proceed to the valet desk in 5 minutes."
    }
