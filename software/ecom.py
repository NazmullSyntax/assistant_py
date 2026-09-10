import datetime


class BookingSystem:
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.users = {}  # {email: name}
        self.bookings = []  # [{id, user_email, date_str, time_slot}]
        self.booking_counter = 1001

        # Available time slots each day
        self.available_slots = [
            "09:00 AM",
            "10:00 AM",
            "11:00 AM",
            "01:00 PM",
            "02:00 PM",
            "03:00 PM",
            "04:00 PM",
        ]

    def register_user(self, name: str, email: str) -> bool:
        """Register a new user by email."""
        if email in self.users:
            print(f"User with email '{email}' already exists.")
            return False
        self.users[email] = name
        print(f"User '{name}' registered successfully!")
        return True

    def get_booked_slots(self, date_str: str) -> list[str]:
        """Return a list of booked slots for a specific date (YYYY-MM-DD)."""
        return [b["time_slot"] for b in self.bookings if b["date_str"] == date_str]

    def view_available_slots(self, date_str: str):
        """Display open time slots for a given date."""
        booked = self.get_booked_slots(date_str)
        print(f"\n--- Available Slots for {date_str} ---")

        open_slots = [s for s in self.available_slots if s not in booked]
        if not open_slots:
            print("Fully booked for this date.")
            return

        for idx, slot in enumerate(open_slots, 1):
            print(f"{idx}. {slot}")

    def create_booking(self, email: str, date_str: str, time_slot: str) -> bool:
        """Book a slot for a registered user."""
        if email not in self.users:
            print("Error: User email not registered.")
            return False

        if time_slot not in self.available_slots:
            print("Error: Invalid time slot selected.")
            return False

        if time_slot in self.get_booked_slots(date_str):
            print(f"Error: The slot {time_slot} on {date_str} is already booked.")
            return False

        booking_id = self.booking_counter
        self.booking_counter += 1

        booking = {
            "id": booking_id,
            "user_email": email,
            "user_name": self.users[email],
            "date_str": date_str,
            "time_slot": time_slot,
        }
        self.bookings.append(booking)
        print(
            f"Success! Booking #{booking_id} confirmed for {self.users[email]} on {date_str} at {time_slot}."
        )
        return True

    def cancel_booking(self, booking_id: int) -> bool:
        """Cancel an existing booking by ID."""
        for booking in self.bookings:
            if booking["id"] == booking_id:
                self.bookings.remove(booking)
                print(f"Booking #{booking_id} cancelled successfully.")
                return True
        print(f"Error: Booking ID #{booking_id} not found.")
        return False

    def list_user_bookings(self, email: str):
        """Show all active bookings for a user."""
        user_bookings = [b for b in self.bookings if b["user_email"] == email]
        if not user_bookings:
            print(f"No bookings found for {email}.")
            return

        print(f"\n--- Bookings for {email} ---")
        for b in user_bookings:
            print(f"ID #{b['id']} | Date: {b['date_str']} | Time: {b['time_slot']}")


# --- Demo Usage ---
if __name__ == "__main__":
    system = BookingSystem("Tech Support Consultation")

    # 1. Register Users
    system.register_user("Alice Smith", "alice@example.com")
    system.register_user("Bob Jones", "bob@example.com")

    # 2. View Open Slots
    date = "2026-04-15"
    system.view_available_slots(date)

    # 3. Create Bookings
    print("\n--- Making Bookings ---")
    system.create_booking("alice@example.com", date, "09:00 AM")

    # Attempt double-booking
    system.create_booking("bob@example.com", date, "09:00 AM")

    # Bob picks another slot
    system.create_booking("bob@example.com", date, "10:00 AM")

    # 4. View Updated Slots & Active Bookings
    system.view_available_slots(date)
    system.list_user_bookings("alice@example.com")

    # 5. Cancel a Booking
    print("\n--- Cancellation Test ---")
    system.cancel_booking(1001)
    system.list_user_bookings("alice@example.com")