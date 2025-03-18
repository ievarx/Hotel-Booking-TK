import tkinter as tk
from tkinter import messagebox
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="hotel_system"
)
cursor = db.cursor()

def make_reservation():
    room_number = room_entry.get()
    guest_name = name_entry.get()
    check_in_date = check_in_entry.get()
    check_out_date = check_out_entry.get()

    if check_availability(room_number, check_in_date, check_out_date):
        sql = "INSERT INTO bookings (room_number, guest_name, check_in_date, check_out_date) VALUES (%s, %s, %s, %s)"
        values = (room_number, guest_name, check_in_date, check_out_date)
        cursor.execute(sql, values)
        db.commit()
        messagebox.showinfo("Reservation Made", "Reservation successfully made!")
        
        # Clear the entry fields
        room_entry.delete(0, 'end')
        name_entry.delete(0, 'end')
        check_in_entry.delete(0, 'end')
        check_out_entry.delete(0, 'end')
    else:
        messagebox.showerror("Error", "Room is already booked for the selected dates.")

def check_availability(room_number, check_in_date, check_out_date):
    sql = f"SELECT COUNT(*) AS count FROM bookings WHERE room_number = {room_number} AND check_in_date <= '{check_out_date}' AND check_out_date >= '{check_in_date}'"
    cursor.execute(sql)
    result = cursor.fetchone()
    count = result[0]
    return count == 0

def query_availability():
    guest_name = guest_name_query_entry.get()

    sql = f"SELECT * FROM bookings WHERE guest_name = '{guest_name}'"
    cursor.execute(sql)
    result = cursor.fetchall()

    if len(result) > 0:
        # Display the reservation details
        details = "\n".join([f"Room Number: {row[1]}, Guest Name: {row[2]}, Check-in Date: {row[3]}, Check-out Date: {row[4]}" for row in result])
        messagebox.showinfo("Reservation Details", details)
    else:
        messagebox.showinfo("Reservation Not Found", f"No reservation found for guest {guest_name}.")

root = tk.Tk()
root.title("Hotel Reservation System")

# Set the size and position of the window
root.geometry("400x400")
root.resizable(False, False)  # Disable resizing

# Create a frame for centering the content
center_frame = tk.Frame(root)
center_frame.pack(expand=True)

# Make Reservation Section
tk.Label(center_frame, text="Make Reservation", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(center_frame, text="Room Number:").grid(row=1, column=0, padx=10, pady=5, sticky="ew")
room_entry = tk.Entry(center_frame)
room_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

tk.Label(center_frame, text="Guest Name:").grid(row=2, column=0, padx=10, pady=5, sticky="ew")
name_entry = tk.Entry(center_frame)
name_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

tk.Label(center_frame, text="Check-in Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5, sticky="ew")
check_in_entry = tk.Entry(center_frame)
check_in_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

tk.Label(center_frame, text="Check-out Date (YYYY-MM-DD):").grid(row=4, column=0, padx=10, pady=5, sticky="ew")
check_out_entry = tk.Entry(center_frame)
check_out_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

reserve_button = tk.Button(center_frame, text="Make Reservation", command=make_reservation)
reserve_button.grid(row=5, column=0, columnspan=2, pady=20, sticky="ew")

# Add extra space between sections
tk.Label(center_frame, text="").grid(row=6, column=0, columnspan=2)

# Query Availability Section
tk.Label(center_frame, text="Query Room Availability", font=("Helvetica", 16)).grid(row=7, column=0, columnspan=2, pady=10)

tk.Label(center_frame, text="Guest Name:").grid(row=8, column=0, padx=10, pady=5, sticky="ew")
guest_name_query_entry = tk.Entry(center_frame)
guest_name_query_entry.grid(row=8, column=1, padx=10, pady=5, sticky="ew")

query_button = tk.Button(center_frame, text="Query Availability", command=query_availability)
query_button.grid(row=9, column=0, columnspan=2, pady=20, sticky="ew")

root.mainloop()
