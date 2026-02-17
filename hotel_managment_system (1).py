import uuid
import datetime

FINE_AMOUNT = 50

def sign_up(users):
    while True:
        username = input("Enter username: ").lower()
        if username in users:
            print("Username exists.")
            continue
        password = input("Enter password: ")
        confirm = input("Confirm password: ")
        if password == confirm:
            users[username] = {
                "password": password,
                "bookings": [],
                "balance": 0,
                "fine": 0,
                "blocked": False
            }
            print("Account created.")
            return
        else:
            print("Passwords do not match.")

def login(users, rooms, bookings):
    username = input("Username: ").lower()
    password = input("Password: ")

    if username == "admin" and password == "Admin@123":
        admin_menu(users, rooms, bookings)
        return

    if username in users and users[username]["password"] == password:
        check_unpaid_bookings(username, users, rooms, bookings)
        user_menu(username, users, rooms, bookings)
    else:
        print("Incorrect username or password.")

def user_menu(username, users, rooms, bookings):
    while True:
        check_unpaid_bookings(username, users, rooms, bookings)

        if users[username]["blocked"]:
            print(f"\nYou are BLOCKED.")
            print(f"Unpaid fine: ${users[username]['fine']}")
            pay = input("Pay fine now? (yes/no): ").lower()
            if pay == "yes":
                users[username]["fine"] = 0
                users[username]["blocked"] = False
                print("Fine paid. You are now unblocked.")
            else:
                print("You remain blocked.")
            return

        choice = input(f"""
===== USER MENU ({username}) =====
1. Book Room
2. Cancel Booking
3. View My Bookings
4. Search Rooms
5. Pay Balance
6. Logout
Choose: """)

        if choice == "1":
            book_room(username, users, rooms, bookings)
        elif choice == "2":
            cancel_booking(username, users, rooms, bookings)
        elif choice == "3":
            show_user_bookings(username, users)
        elif choice == "4":
            search_room(rooms)
        elif choice == "5":
            pay_balance(username, users, bookings)
        elif choice == "6":
            break

def check_unpaid_bookings(username, users, rooms, bookings):
    today = datetime.date.today()
    to_remove = []

    for booking in list(users[username]["bookings"]):
        if not booking["paid"] and today > booking["check_in"]:
            room = booking["room"]
            rooms[room]["available"] = True
            users[username]["fine"] += FINE_AMOUNT
            users[username]["blocked"] = True
            to_remove.append(booking)
            print(f"\nBooking for room {room} automatically cancelled.")
            print("Fine applied for unpaid booking.")

    for b in to_remove:
        users[username]["bookings"].remove(b)
        for gb in list(bookings):
            if gb.get("booking_id") == b.get("booking_id") and gb.get("user") == username:
                bookings.remove(gb)

def pay_balance(username, users, bookings):
    balance = users[username]["balance"]
    if balance == 0:
        print("No outstanding balance.")
        return

    print(f"Balance: ${balance}")
    pay = input("Pay now? (yes/no): ").lower()

    if pay == "yes":
        users[username]["balance"] = 0

        for ub in users[username]["bookings"]:
            if not ub.get("paid"):
                ub["paid"] = True
                for gb in bookings:
                    if gb.get("booking_id") == ub.get("booking_id") and gb.get("user") == username:
                        gb["paid"] = True

        print("Payment completed. All your bookings are marked as paid.")
    else:
        print("Payment canceled.")

def book_room(username, users, rooms, bookings):
    print("\nAvailable rooms:")
    for r in rooms:
        if rooms[r]["available"]:
            print(f"{r} - ${rooms[r]['price']} per night")

    room = input("Choose room: ")
    if room not in rooms or not rooms[room]["available"]:
        print("Room unavailable.")
        return

    try:
        nights = int(input("Number of nights: "))
    except:
        print("Invalid number of nights.")
        return

    try:
        date_str = input("Enter check-in date (YYYY-MM-DD): ")
        check_in = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        if check_in < datetime.date.today():
            print("Check-in date cannot be in the past.")
            return
    except:
        print("Invalid date.")
        return

    check_out = check_in + datetime.timedelta(days=nights)
    cost = nights * rooms[room]["price"]
    booking_id = str(uuid.uuid4())[:8]

    record = {
        "booking_id": booking_id,
        "room": room,
        "check_in": check_in,
        "check_out": check_out,
        "nights": nights,
        "total_cost": cost,
        "paid": False
    }

    users[username]["bookings"].append(record)
    bookings.append({"user": username, **record})
    rooms[room]["available"] = False
    users[username]["balance"] += cost

    print(f"""
Booking successful.

Booking ID : {booking_id}
Room       : {room}
Check-In   : {check_in}
Check-Out  : {check_out}
Total Cost : ${cost}
""")

def cancel_booking(username, users, rooms, bookings):
    user_bookings = users[username]["bookings"]

    if not user_bookings:
        print("No bookings.")
        return

    print("\nYour bookings:")
    for i, b in enumerate(user_bookings, 1):
        print(f"{i}. Room {b['room']} | ID: {b['booking_id']} | Paid: {b['paid']}")

    try:
        choice = int(input("Choose: ")) - 1
    except:
        print("Invalid selection.")
        return

    if 0 <= choice < len(user_bookings):
        b = user_bookings[choice]

        if b["paid"]:
            print("Paid bookings cannot be canceled.")
            return

        rooms[b["room"]]["available"] = True
        users[username]["balance"] -= b["total_cost"]
        user_bookings.pop(choice)

        for gb in list(bookings):
            if gb.get("booking_id") == b.get("booking_id") and gb.get("user") == username:
                bookings.remove(gb)

        print("Booking canceled.")
    else:
        print("Invalid selection.")

def search_room(rooms):
    term = input("Search by type: ").lower()
    results = [r for r in rooms if rooms[r]["type"].lower() == term]

    print("Found:" if results else "No results.")
    for r in results:
        print(f"{r} - ${rooms[r]['price']} - {'Available' if rooms[r]['available'] else 'Occupied'}")

def show_user_bookings(username, users):
    b = users[username]["bookings"]

    if not b:
        print("No bookings.")
        return

    for x in b:
        print(f"""
Booking ID: {x['booking_id']}
Room: {x['room']}
Check-In: {x['check_in']}
Check-Out: {x['check_out']}
Nights: {x['nights']}
Cost: ${x['total_cost']}
Paid: {x['paid']}
""")

def admin_menu(users, rooms, bookings):
    while True:
        choice = input("""
===== ADMIN MENU =====
1. Add Room
2. Remove Room
3. View All Bookings
4. View Users
5. Logout
Choose: """)

        if choice == "1":
            add_room(rooms)
        elif choice == "2":
            remove_room(rooms)
        elif choice == "3":
            show_all_bookings(bookings)
        elif choice == "4":
            manage_users(users)
        elif choice == "5":
            break

def add_room(rooms):
    number = input("Room number: ")

    if number in rooms:
        print("Exists.")
        return

    rtype = input("Type (single/double/suite): ")

    try:
        price = int(input("Price per night: "))
    except:
        print("Invalid price.")
        return

    rooms[number] = {"type": rtype, "price": price, "available": True}
    print("Room added.")

def remove_room(rooms):
    number = input("Room to remove: ")

    if number in rooms:
        del rooms[number]
        print("Removed.")
    else:
        print("Not found.")

def show_all_bookings(bookings):
    if not bookings:
        print("No bookings.")
        return

    for b in bookings:
        print(f"{b['user']} → Room {b['room']} | ID: {b['booking_id']} | Check-In: {b['check_in']} | Paid: {b.get('paid', False)}")

def manage_users(users):
    print("\nUsers:")
    for u in users:
        print(f"{u} | Balance: {users[u]['balance']} | Fine: {users[u]['fine']} | Blocked: {users[u]['blocked']}")

    delete = input("Delete user (Enter to skip): ").lower()

    if delete and delete in users:
        del users[delete]
        print("Deleted.")

def main():
    users = {}
    rooms = {
        "101": {"type": "single", "price": 100, "available": True},
        "102": {"type": "double", "price": 150, "available": True},
        "201": {"type": "suite", "price": 300, "available": True}
    }
    bookings = []

    print("Welcome to the Hotel System.")

    while True:
        choice = input("""
1. Login
2. Sign Up
3. Exit
Choose: """)

        if choice == "1":
            login(users, rooms, bookings)
        elif choice == "2":
            sign_up(users)
        elif choice == "3":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()