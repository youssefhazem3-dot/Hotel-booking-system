# Hotel Management System (HMS)

## 📌 Overview
This project is a CLI-based Hotel Management System developed in Python. It provides a complete workflow for both administrators and customers, including room booking, real-time availability tracking, and a unique **automatic penalty system** for unpaid reservations.

The project features a modular structure with automated date-checking logic to ensure hotel policy compliance.

---

## 🚀 Features

### **👤 Customer Portal**
* **Account Creation**: Secure sign-up and login functionality with password confirmation.
* **Room Booking**: Real-time room selection with cost calculation based on the number of nights.
* **Automated Fine System**: Users are automatically **blocked** and fined **$50** if a booking remains unpaid past the check-in date.
* **Booking Management**: Users can view their full booking history or cancel unpaid reservations.
* **Centralized Billing**: A "Pay Balance" feature allows users to clear all outstanding costs and unblock their accounts.

### **🛡️ Admin Portal**
* **Room Inventory**: Add new rooms with specific types (single, double, suite) and prices, or remove existing rooms.
* **Global Monitoring**: View every booking made in the system, including user details and payment status.
* **User Oversight**: Monitor user balances, active fines, and block status; includes the ability to delete user accounts.

---

## 🛠️ Technologies Used
* **Python 3.x**: Core logic and system functions.
* **Datetime Module**: Powering the automated check-in validation and fine triggers.
* **UUID Module**: Used to generate unique 8-character identifiers for every booking.
* **Standard Library**: Built with no external dependencies for maximum portability.

---

## 📂 Project Structure
```text
N.N project code/
├── hotel_managment_system.py  # Main script containing all system logic
└── README.md                  # Project documentation
```
## ▶️ Usage
### **Admin Access**
To access the admin dashboard, use the following default credentials:

Username: admin

Password: Admin@123

### **Customer Workflow**
Sign Up: Create a new account to begin using the system.

Search: Find available rooms by type (e.g., "suite").

Book: Select check-in date and duration for your stay; the system prevents bookings in the past.

Pay: Use the Pay Balance option before your check-in date to avoid being blocked.

---

## 🎯 Learning Objectives
Implementing complex conditional logic for user status, such as distinguishing between Blocked and Active accounts.

Managing relational-style data using Python dictionaries and lists.

Automating date-based triggers, specifically for automatic cancellations and fine applications.

Creating a secure Admin/User permission system.

---

## 👤 Author
Yousef Hazem

---

## 📄 License
This project is intended for educational purposes.
