import json
from datetime import datetime, date, timedelta
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "appointments.json"
REMINDER_DAYS = 2


# Load saved appointments
def load_appointments():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []
    return []


# Save appointments permanently
def save_appointments(appointments):
    with open(DATA_FILE, "w") as f:
        json.dump(appointments, f, indent=4)


# Select purpose
def choose_purpose():
    print("\n--- Appointment Purpose ---")
    print("1. Fever")
    print("2. Eye Checkup")
    print("3. Dental Checkup")
    print("4. Headache")
    print("5. General Checkup")
    print("6. Other")

    choice = input("Select purpose: ")

    purposes = {
        "1": "Fever",
        "2": "Eye Checkup",
        "3": "Dental Checkup",
        "4": "Headache",
        "5": "General Checkup",
        "6": "Other"
    }

    if choice in purposes:
        return purposes[choice]

    print("Invalid choice!")
    return choose_purpose()


# Check whether slot is already booked
def is_slot_taken(appointments, appt_date, appt_time):
    for a in appointments:
        if (a["date"] == appt_date and
                a["time"] == appt_time and
                a["status"] == "Booked"):
            return True
    return False


# Book appointment
def book_appointment(appointments):
    print("\n--- Book Appointment ---")

    name = input("Enter patient name: ").strip()

    if not name:
        print("Name cannot be empty!")
        return

    phone = input("Enter 10-digit phone number: ").strip()

    if not phone.isdigit() or len(phone) != 10:
        print("Invalid phone number!")
        return

    try:
        appt_date = input("Enter date (YYYY-MM-DD): ").strip()
        date_obj = datetime.strptime(appt_date, "%Y-%m-%d").date()

        if date_obj < date.today():
            print("Past date is not allowed!")
            return

    except ValueError:
        print("Invalid date format!")
        return

    try:
        appt_time = input("Enter time (HH:MM): ").strip()
        datetime.strptime(appt_time, "%H:%M")

    except ValueError:
        print("Invalid time! Use HH:MM format.")
        return

    if is_slot_taken(appointments, appt_date, appt_time):
        print("This time slot is already booked!")
        return

    purpose = choose_purpose()

    new_id = max([a["id"] for a in appointments], default=0) + 1

    new_appointment = {
        "id": new_id,
        "name": name,
        "phone": phone,
        "date": appt_date,
        "time": appt_time,
        "purpose": purpose,
        "status": "Booked"
    }

    appointments.append(new_appointment)
    save_appointments(appointments)

    print("\nAppointment booked successfully!")
    print("Appointment ID:", new_id)


# View all appointments
def view_appointments(appointments):
    print("\n--- All Appointments ---")

    active = [a for a in appointments if a["status"] == "Booked"]

    if not active:
        print("No appointments found.")
        return

    active.sort(key=lambda a: (a["date"], a["time"]))

    for a in active:
        print("\nID:", a["id"])
        print("Name:", a["name"])
        print("Phone:", a["phone"])
        print("Date:", a["date"])
        print("Time:", a["time"])
        print("Purpose:", a["purpose"])
        print("Status:", a["status"])


# Cancel appointment
def cancel_appointment(appointments):
    print("\n--- Cancel Appointment ---")

    try:
        appt_id = int(input("Enter appointment ID: "))
    except ValueError:
        print("Enter a valid ID!")
        return

    for a in appointments:
        if a["id"] == appt_id and a["status"] == "Booked":
            a["status"] = "Cancelled"
            save_appointments(appointments)
            print("Appointment cancelled successfully!")
            return

    print("Appointment not found!")


# Search appointment
def search_appointment(appointments):
    print("\n--- Search Appointment ---")

    name = input("Enter patient name: ").strip().lower()

    found = False

    for a in appointments:
        if name in a["name"].lower() and a["status"] == "Booked":
            print("\nID:", a["id"])
            print("Name:", a["name"])
            print("Phone:", a["phone"])
            print("Date:", a["date"])
            print("Time:", a["time"])
            print("Purpose:", a["purpose"])
            print("Status:", a["status"])
            found = True

    if not found:
        print("No appointment found!")


# Show reminders
def show_reminders(appointments):
    today = date.today()
    end_date = today + timedelta(days=REMINDER_DAYS)

    print("\n--- Appointment Reminders ---")

    found = False

    for a in appointments:
        if a["status"] != "Booked":
            continue

        appt_date = datetime.strptime(a["date"], "%Y-%m-%d").date()

        if today <= appt_date <= end_date:
            print("\nID:", a["id"])
            print("Name:", a["name"])
            print("Date:", a["date"])
            print("Time:", a["time"])
            print("Purpose:", a["purpose"])
            found = True

    if not found:
        print("No upcoming appointments in the next 2 days.")


# Main menu
def main():
    appointments = load_appointments()

    print("\n================================")
    print(" DOCTOR CLINIC APPOINTMENT SYSTEM")
    print("================================")

    show_reminders(appointments)

    while True:
        print("\n--- Main Menu ---")
        print("1. Book Appointment")
        print("2. View Appointments")
        print("3. Cancel Appointment")
        print("4. Search Appointment")
        print("5. Show Reminders")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            book_appointment(appointments)

        elif choice == "2":
            view_appointments(appointments)

        elif choice == "3":
            cancel_appointment(appointments)

        elif choice == "4":
            search_appointment(appointments)

        elif choice == "5":
            show_reminders(appointments)

        elif choice == "6":
            print("Thank you for using the Appointment System!")
            break

        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()
