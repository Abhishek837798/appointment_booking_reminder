"""
Appointment Booking and Reminder System
---------------------------------------
Python Mini Project - BCA, MRIIRS
Made by: Abhishek (Roll No: 25/SCA/BCOA/005)

What it does:
  * Book an appointment (name, phone, date, time, purpose)
  * Stop two people from booking the same date + time
  * View all appointments
  * Cancel an appointment
  * Show reminders for today and the next few days
  * Search appointments by name

All data is saved in a small file (appointments.json), so nothing is
lost when the program is closed.
"""

import json
from datetime import datetime, date, timedelta

DATA_FILE = "appointments.json"   # the file where we keep everything
REMINDER_DAYS = 2                 # remind about appointments in the next 2 days


# ---------------------------------------------------------------
# Part 1: Saving and loading data
# ---------------------------------------------------------------
def load_appointments():
    """Read all appointments from the file. If there is no file yet, start empty."""
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_appointments(appointments):
    """Write the full list of appointments back to the file."""
    with open(DATA_FILE, "w") as f:
        json.dump(appointments, f, indent=4)


# ---------------------------------------------------------------
# Part 2: Small helper functions
# ---------------------------------------------------------------
def get_next_id(appointments):
    """Give every new appointment a number: 1, 2, 3 ..."""
    if len(appointments) == 0:
        return 1
    return max(a["id"] for a in appointments) + 1


def ask_date():
    """Keep asking until the user types a valid date that is not in the past."""
    while True:
        text = input("Enter date (YYYY-MM-DD): ").strip()
        try:
            chosen = datetime.strptime(text, "%Y-%m-%d").date()
        except ValueError:
            print("  Oops! That is not a valid date. Example: 2026-11-25")
            continue
        if chosen < date.today():
            print("  That date is already over. Please pick today or a future date.")
            continue
        return text


def ask_time():
    """Keep asking until the user types a valid time in 24-hour format."""
    while True:
        text = input("Enter time (HH:MM, 24-hour): ").strip()
        try:
            datetime.strptime(text, "%H:%M")
            return text
        except ValueError:
            print("  Oops! Please type the time like 14:30")


def is_slot_taken(appointments, day, time):
    """Check if someone has already booked this date and time (and not cancelled)."""
    for a in appointments:
        if a["date"] == day and a["time"] == time and a["status"] == "Booked":
            return True
    return False


def print_appointment(a):
    """Print one appointment in a neat line."""
    print(f"  #{a['id']} | {a['date']} {a['time']} | {a['name']} "
          f"({a['phone']}) | {a['purpose']} | {a['status']}")


# ---------------------------------------------------------------
# Part 3: The main features
# ---------------------------------------------------------------
def book_appointment(appointments):
    print("\n--- Book a New Appointment ---")
    name = input("Enter your name: ").strip()
    if name == "":
        print("  Name cannot be empty.")
        return

    phone = input("Enter phone number (10 digits): ").strip()
    if not (phone.isdigit() and len(phone) == 10):
        print("  Phone number must be exactly 10 digits.")
        return

    day = ask_date()
    time = ask_time()

    # make sure nobody else has this slot
    if is_slot_taken(appointments, day, time):
        print("  Sorry, that slot is already booked. Please try another time.")
        return

    purpose = input("Purpose of visit: ").strip()
    if purpose == "":
        purpose = "General"

    new_appointment = {
        "id": get_next_id(appointments),
        "name": name,
        "phone": phone,
        "date": day,
        "time": time,
        "purpose": purpose,
        "status": "Booked",
    }
    appointments.append(new_appointment)
    save_appointments(appointments)
    print(f"  Done! Appointment #{new_appointment['id']} booked for {day} at {time}.")


def view_appointments(appointments):
    print("\n--- All Appointments ---")
    if len(appointments) == 0:
        print("  No appointments yet.")
        return
    # sort by date first, then by time
    for a in sorted(appointments, key=lambda x: (x["date"], x["time"])):
        print_appointment(a)


def cancel_appointment(appointments):
    print("\n--- Cancel an Appointment ---")
    text = input("Enter the appointment number to cancel: ").strip()
    if not text.isdigit():
        print("  Please type a number.")
        return

    number = int(text)
    for a in appointments:
        if a["id"] == number:
            if a["status"] == "Cancelled":
                print("  This appointment is already cancelled.")
            else:
                a["status"] = "Cancelled"
                save_appointments(appointments)
                print(f"  Appointment #{number} has been cancelled.")
            return
    print("  No appointment found with that number.")


def show_reminders(appointments):
    print("\n--- Reminders ---")
    today = date.today()
    last_day = today + timedelta(days=REMINDER_DAYS)
    found = False

    for a in sorted(appointments, key=lambda x: (x["date"], x["time"])):
        if a["status"] != "Booked":
            continue  # cancelled ones need no reminder
        appt_day = datetime.strptime(a["date"], "%Y-%m-%d").date()
        if today <= appt_day <= last_day:
            found = True
            if appt_day == today:
                when = "TODAY"
            elif appt_day == today + timedelta(days=1):
                when = "TOMORROW"
            else:
                when = "on " + a["date"]
            print(f"  Reminder: {a['name']} has an appointment {when} "
                  f"at {a['time']} for {a['purpose']}.")

    if not found:
        print(f"  No upcoming appointments in the next {REMINDER_DAYS} days.")


def search_by_name(appointments):
    print("\n--- Search by Name ---")
    word = input("Enter name to search: ").strip().lower()
    found = False
    for a in appointments:
        if word in a["name"].lower():
            print_appointment(a)
            found = True
    if not found:
        print("  No matching appointments.")


# ---------------------------------------------------------------
# Part 4: The menu (this is where the program starts)
# ---------------------------------------------------------------
def main():
    appointments = load_appointments()
    print("=" * 45)
    print("   APPOINTMENT BOOKING & REMINDER SYSTEM")
    print("=" * 45)

    # show reminders as soon as the program opens
    show_reminders(appointments)

    while True:
        print("\n1. Book appointment")
        print("2. View all appointments")
        print("3. Cancel appointment")
        print("4. Show reminders")
        print("5. Search by name")
        print("6. Exit")
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            book_appointment(appointments)
        elif choice == "2":
            view_appointments(appointments)
        elif choice == "3":
            cancel_appointment(appointments)
        elif choice == "4":
            show_reminders(appointments)
        elif choice == "5":
            search_by_name(appointments)
        elif choice == "6":
            print("Thank you! Goodbye.")
            break
        else:
            print("  Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
