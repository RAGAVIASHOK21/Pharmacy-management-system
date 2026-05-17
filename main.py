import sqlite3
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk, ImageEnhance  # Import ImageEnhance for adjusting opacity

# Database setup
conn = sqlite3.connect("pharmacy.db")
cursor = conn.cursor()

# Create necessary tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS admin (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    emp_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    salary REAL NOT NULL,
    position TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS medicines (
    med_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    stock INT NOT NULL
)
''')

conn.commit()

# ------------------------- Admin Login --------------------------

def login_window():
    def login():
        user = username_entry.get()
        pwd = password_entry.get()
        cursor.execute("SELECT * FROM admin WHERE username=? AND password=?", (user, pwd))
        if cursor.fetchone():
            win.destroy()
            main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    win = Tk()
    win.geometry("1920x1080")
    win.title("Admin Login")
    win.config(bg="#f0f8ff")

    Label(win, text="Admin Login", bg="#f0f8ff", font=("Arial", 32, "bold")).pack(pady=40)
    Label(win, text="Username", bg="#f0f8ff", font=("Arial", 20)).pack(pady=20)
    username_entry = Entry(win, font=("Arial", 20), width=30)
    username_entry.pack(pady=10)

    Label(win, text="Password", bg="#f0f8ff", font=("Arial", 20)).pack(pady=20)
    password_entry = Entry(win, show="*", font=("Arial", 20), width=30)
    password_entry.pack(pady=10)

    Button(win, text="Login", command=login, width=20, height=2, bg="#4CAF50", fg="white", font=("Arial", 20)).pack(pady=40)
    win.mainloop()

# ------------------------- Main Menu --------------------------

def main_menu():
    def add_employee_window():
        def add_employee():
            emp_id = emp_id_entry.get()
            name = name_entry.get()
            salary = salary_entry.get()
            position = position_entry.get()

            if not emp_id or not name or not salary or not position:
                messagebox.showwarning("Input Error", "Please fill in all fields")
                return

            cursor.execute("INSERT INTO employees (emp_id, name, salary, position) VALUES (?, ?, ?, ?)",
                           (emp_id, name, float(salary), position))
            conn.commit()
            messagebox.showinfo("Success", "Employee added successfully")
            add_win.destroy()

        add_win = Toplevel()
        add_win.geometry("1920x1080")
        add_win.title("Add Employee")
        add_win.config(bg="#e6f7ff")

        Label(add_win, text="Add Employee", bg="#e6f7ff", font=("Arial", 32, "bold")).pack(pady=40)
        Label(add_win, text="Employee ID", bg="#e6f7ff", font=("Arial", 20)).pack(pady=20)
        emp_id_entry = Entry(add_win, font=("Arial", 20), width=30)
        emp_id_entry.pack(pady=10)

        Label(add_win, text="Name", bg="#e6f7ff", font=("Arial", 20)).pack(pady=20)
        name_entry = Entry(add_win, font=("Arial", 20), width=30)
        name_entry.pack(pady=10)

        Label(add_win, text="Salary", bg="#e6f7ff", font=("Arial", 20)).pack(pady=20)
        salary_entry = Entry(add_win, font=("Arial", 20), width=30)
        salary_entry.pack(pady=10)

        Label(add_win, text="Position", bg="#e6f7ff", font=("Arial", 20)).pack(pady=20)
        position_entry = Entry(add_win, font=("Arial", 20), width=30)
        position_entry.pack(pady=10)

        Button(add_win, text="Add Employee", command=add_employee, width=25, height=2, bg="#4CAF50", fg="white", font=("Arial", 20)).pack(pady=40)

    def view_employees():
        cursor.execute("SELECT * FROM employees")
        data = cursor.fetchall()

        if not data:
            messagebox.showinfo("No Data", "No employee records found.")
            return

        win = Toplevel()
        win.geometry("1920x1080")
        win.title("View Employees")
        win.config(bg="#f5f5f5")

        Label(win, text="Employee Records", bg="#f5f5f5", font=("Arial", 32, "bold")).pack(pady=40)
        text_widget = Text(win, width=120, height=30, font=("Arial", 16))
        text_widget.pack(pady=20)
        text_widget.insert(END, f"{'Employee ID':<20} {'Name':<30} {'Salary':<20} {'Position':<30}\n")
        text_widget.insert(END, "-"*100 + "\n")

        for row in data:
            text_widget.insert(END, f"{row[0]:<20} {row[1]:<30} {row[2]:<20} {row[3]:<30}\n")

    def edit_employee_window():
        def search_employee():
            emp_id = emp_id_entry.get()
            cursor.execute("SELECT * FROM employees WHERE emp_id=?", (emp_id,))
            employee = cursor.fetchone()
            if employee:
                name_entry.delete(0, END)
                salary_entry.delete(0, END)
                position_entry.delete(0, END)
                name_entry.insert(0, employee[1])
                salary_entry.insert(0, str(employee[2]))
                position_entry.insert(0, employee[3])
                edit_btn.config(state=NORMAL)
            else:
                messagebox.showerror("Error", "Employee not found")
                name_entry.delete(0, END)
                salary_entry.delete(0, END)
                position_entry.delete(0, END)
                edit_btn.config(state=DISABLED)

        def edit_employee():
            emp_id = emp_id_entry.get()
            name = name_entry.get()
            salary = salary_entry.get()
            position = position_entry.get()

            if name and salary and position:
                cursor.execute("UPDATE employees SET name=?, salary=?, position=? WHERE emp_id=?",
                               (name, float(salary), position, emp_id))
                conn.commit()
                messagebox.showinfo("Success", "Employee updated successfully")
                edit_win.destroy()
            else:
                messagebox.showwarning("Input Error", "Please fill in all fields.")

        edit_win = Toplevel()
        edit_win.geometry("1920x1080")
        edit_win.title("Edit Employee")
        edit_win.config(bg="#e6f7ff")

        Label(edit_win, text="Edit Employee", bg="#e6f7ff", font=("Arial", 32, "bold")).pack(pady=40)
        Label(edit_win, text="Employee ID", bg="#e6f7ff", font=("Arial", 20)).pack(pady=20)
        emp_id_entry = Entry(edit_win, font=("Arial", 20), width=30)
        emp_id_entry.pack(pady=10)

        Button(edit_win, text="Search", command=search_employee, width=15, height=1, bg="#2196F3", fg="white", font=("Arial", 16)).pack(pady=10)

        Label(edit_win, text="Name", bg="#e6f7ff", font=("Arial", 20)).pack(pady=20)
        name_entry = Entry(edit_win, font=("Arial", 20), width=30)
        name_entry.pack(pady=10)

        Label(edit_win, text="Salary", bg="#e6f7ff", font=("Arial", 20)).pack(pady=20)
        salary_entry = Entry(edit_win, font=("Arial", 20), width=30)
        salary_entry.pack(pady=10)

        Label(edit_win, text="Position", bg="#e6f7ff", font=("Arial", 20)).pack(pady=20)
        position_entry = Entry(edit_win, font=("Arial", 20), width=30)
        position_entry.pack(pady=10)

        edit_btn = Button(edit_win, text="Update Employee", command=edit_employee, width=25, height=2, bg="#ff9800", fg="white", font=("Arial", 20), state=DISABLED)
        edit_btn.pack(pady=40)

    def delete_employee_window():
        def delete_employee():
            emp_id = emp_id_entry.get()
            cursor.execute("DELETE FROM employees WHERE emp_id=?", (emp_id,))
            conn.commit()
            messagebox.showinfo("Deleted", "Employee deleted successfully")
            delete_win.destroy()

        delete_win = Toplevel()
        delete_win.geometry("1920x1080")
        delete_win.title("Delete Employee")
        delete_win.config(bg="#ffebee")

        Label(delete_win, text="Delete Employee", bg="#ffebee", font=("Arial", 32, "bold")).pack(pady=40)
        Label(delete_win, text="Employee ID", bg="#ffebee", font=("Arial", 20)).pack(pady=20)
        emp_id_entry = Entry(delete_win, font=("Arial", 20), width=30)
        emp_id_entry.pack(pady=10)

        Button(delete_win, text="Delete Employee", command=delete_employee, width=25, height=2, bg="#f44336", fg="white", font=("Arial", 20)).pack(pady=40)

    def add_medicine_window():
        def add_medicine():
            med_id = med_id_entry.get()
            name = name_entry.get()
            category = category_entry.get()
            price = price_entry.get()
            stock = stock_entry.get()

            if not med_id or not name or not category or not price or not stock:
                messagebox.showwarning("Input Error", "Please fill in all fields.")
                return

            try:
                cursor.execute("INSERT INTO medicines (med_id, name, category, price, stock) VALUES (?, ?, ?, ?, ?)",
                               (med_id, name, category, float(price), int(stock)))
                conn.commit()
                messagebox.showinfo("Success", "Medicine added successfully.")
                add_win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add medicine: {e}")

        add_win = Toplevel()
        add_win.geometry("1920x1080")
        add_win.title("Add Medicine")
        add_win.config(bg="#e6f7ff")

        Label(add_win, text="Add Medicine", bg="#e6f7ff", font=("Arial", 32, "bold")).pack(pady=40)
        Label(add_win, text="Medicine ID", bg="#e6f7ff", font=("Arial", 20)).pack(pady=20)
        med_id_entry = Entry(add_win, font=("Arial", 20), width=30)
        med_id_entry.pack(pady=10)

        Label(add_win, text="Name", bg="#e6f7ff", font=("Arial", 20)).pack(pady=20)
        name_entry = Entry(add_win, font=("Arial", 20), width=30)
        name_entry.pack(pady=10)

        Label(add_win, text="Category", bg="#e6f7ff", font=("Arial", 20)).pack(pady=20)
        category_entry = Entry(add_win, font=("Arial", 20), width=30)
        category_entry.pack(pady=10)

        Label(add_win, text="Price", bg="#e6f7ff", font=("Arial", 20)).pack(pady=20)
        price_entry = Entry(add_win, font=("Arial", 20), width=30)
        price_entry.pack(pady=10)

        Label(add_win, text="Stock", bg="#e6f7ff", font=("Arial", 20)).pack(pady=20)
        stock_entry = Entry(add_win, font=("Arial", 20), width=30)
        stock_entry.pack(pady=10)

        Button(add_win, text="Add Medicine", command=add_medicine, width=25, height=2, bg="#4CAF50", fg="white", font=("Arial", 20)).pack(pady=40)

    def view_medicines():
        cursor.execute("SELECT * FROM medicines")
        data = cursor.fetchall()

        if not data:
            messagebox.showinfo("No Data", "No medicine records found.")
            return

        win = Toplevel()
        win.geometry("1920x1080")
        win.title("View Medicines")
        win.config(bg="#f5f5f5")

        Label(win, text="Medicine Records", bg="#f5f5f5", font=("Arial", 32, "bold")).pack(pady=40)

        # Create a Text widget for displaying the table
        text_widget = Text(win, width=120, height=30, font=("Courier", 16), bg="#ffffff", fg="#000000")
        text_widget.pack(pady=20)

        # Add table headers with proper alignment
        headers = f"{'Medicine ID':<20}{'Name':<30}{'Category':<20}{'Price':<15}{'Stock':<10}\n"
        text_widget.insert(END, headers)
        text_widget.insert(END, "-" * 100 + "\n")

        # Add data rows with proper alignment
        for row in data:
            row_data = f"{row[0]:<20}{row[1]:<30}{row[2]:<20}{row[3]:<15.2f}{row[4]:<10}\n"
            text_widget.insert(END, row_data)

        # Disable editing in the Text widget
        text_widget.config(state=DISABLED)

    def edit_medicine_window():
        def edit_medicine():
            med_id = med_id_entry.get()
            cursor.execute("SELECT * FROM medicines WHERE med_id=?", (med_id,))
            medicine = cursor.fetchone()

            if not medicine:
                messagebox.showerror("Error", "Medicine not found")
                return

            name = name_entry.get()
            category = category_entry.get()
            price = price_entry.get()
            stock = stock_entry.get()

            if name and category and price and stock:
                cursor.execute("UPDATE medicines SET name=?, category=?, price=?, stock=? WHERE med_id=?",
                               (name, category, float(price), int(stock), med_id))
                conn.commit()
                messagebox.showinfo("Success", "Medicine updated successfully")
                edit_win.destroy()

        edit_win = Toplevel()
        edit_win.geometry("1920x1080")
        edit_win.title("Edit Medicine")
        edit_win.config(bg="#e6f7ff")

        Label(edit_win, text="Edit Medicine", bg="#e6f7ff", font=("Arial", 32, "bold")).pack(pady=40)
        Label(edit_win, text="Medicine ID", bg="#e6f7ff", font=("Arial", 20)).pack(pady=20)
        med_id_entry = Entry(edit_win, font=("Arial", 20), width=30)
        med_id_entry.pack(pady=10)

        Label(edit_win, text="Name", bg="#e6f7ff", font=("Arial", 20)).pack(pady=20)
        name_entry = Entry(edit_win, font=("Arial", 20), width=30)
        name_entry.pack(pady=10)

        Label(edit_win, text="Category", bg="#e6f7ff", font=("Arial", 20)).pack(pady=20)
        category_entry = Entry(edit_win, font=("Arial", 20), width=30)
        category_entry.pack(pady=10)

        Label(edit_win, text="Price", bg="#e6f7ff", font=("Arial", 20)).pack(pady=20)
        price_entry = Entry(edit_win, font=("Arial", 20), width=30)
        price_entry.pack(pady=10)

        Label(edit_win, text="Stock", bg="#e6f7ff", font=("Arial", 20)).pack(pady=20)
        stock_entry = Entry(edit_win, font=("Arial", 20), width=30)
        stock_entry.pack(pady=10)

        Button(edit_win, text="Update Medicine", command=edit_medicine, width=25, height=2, bg="#ff9800", fg="white", font=("Arial", 20)).pack(pady=40)

    def delete_medicine_window():
        def delete_medicine():
            med_id = med_id_entry.get()
            if not med_id:
                messagebox.showwarning("Input Error", "Please enter a Medicine ID.")
                return

            cursor.execute("SELECT * FROM medicines WHERE med_id=?", (med_id,))
            medicine = cursor.fetchone()

            if not medicine:
                messagebox.showerror("Error", "Medicine not found.")
                return

            response = messagebox.askyesno("Confirmation", f"Are you sure you want to delete Medicine ID: {med_id}?")
            if response:
                cursor.execute("DELETE FROM medicines WHERE med_id=?", (med_id,))
                conn.commit()
                messagebox.showinfo("Deleted", "Medicine deleted successfully.")
                delete_win.destroy()

        delete_win = Toplevel()
        delete_win.geometry("1920x1080")
        delete_win.title("Delete Medicine")
        delete_win.config(bg="#ffebee")

        Label(delete_win, text="Delete Medicine", bg="#ffebee", font=("Arial", 32, "bold")).pack(pady=40)
        Label(delete_win, text="Medicine ID", bg="#ffebee", font=("Arial", 20)).pack(pady=20)
        med_id_entry = Entry(delete_win, font=("Arial", 20), width=30)
        med_id_entry.pack(pady=10)

        Button(delete_win, text="Delete Medicine", command=delete_medicine, width=25, height=2, bg="#f44336", fg="white", font=("Arial", 20)).pack(pady=40)

    # Main menu window
    main_win = Tk()
    main_win.geometry("1920x1080")
    main_win.title("Pharmacy Management System")

    # Load and set the background image with 50% opacity
    try:
        bg_image = Image.open("image.jpg")  # Replace with the correct path to your image
        bg_image = bg_image.resize((1920, 1080), Image.Resampling.LANCZOS)  # Resize the image

        # Apply 50% opacity
        enhancer = ImageEnhance.Brightness(bg_image.convert("RGBA"))
        bg_image = enhancer.enhance(0.5)  # Reduce brightness to simulate opacity

        bg_photo = ImageTk.PhotoImage(bg_image)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load background image: {e}")
        return

    bg_label = Label(main_win, image=bg_photo)
    bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
    bg_label.place(relwidth=1, relheight=1)  # Cover the entire window with the image

    # Title label
    Label(main_win, text="Pharmacy Management System", font=('Arial', 36, 'bold'), bg="#ffffff", fg="#000000").pack(pady=30)

    # Buttons
    Button(main_win, text="Add Employee", width=40, height=2, command=add_employee_window, bg="#4CAF50", fg="white", font=("Arial", 18)).pack(pady=15)
    Button(main_win, text="View Employees", width=40, height=2, command=view_employees, bg="#2196F3", fg="white", font=("Arial", 18)).pack(pady=15)
    Button(main_win, text="Edit Employee", width=40, height=2, command=edit_employee_window, bg="#FF9800", fg="white", font=("Arial", 18)).pack(pady=15)
    Button(main_win, text="Delete Employee", width=40, height=2, command=delete_employee_window, bg="#F44336", fg="white", font=("Arial", 18)).pack(pady=15)
    Button(main_win, text="Add Medicine", width=40, height=2, command=add_medicine_window, bg="#4CAF50", fg="white", font=("Arial", 18)).pack(pady=15)
    Button(main_win, text="View Medicines", width=40, height=2, command=view_medicines, bg="#2196F3", fg="white", font=("Arial", 18)).pack(pady=15)
    Button(main_win, text="Delete Medicine", width=40, height=2, command=delete_medicine_window, bg="#F44336", fg="white", font=("Arial", 18)).pack(pady=15)
    Button(main_win, text="Logout", width=40, height=2, command=lambda: (main_win.destroy(), login_window()), bg="#9E9E9E", fg="white", font=("Arial", 18)).pack(pady=15)

    main_win.mainloop()

# Information Message Box
def show_info_message():
    messagebox.showinfo("Information", "This is an informational message.")

# Warning Message Box
def show_warning_message():
    messagebox.showwarning("Warning", "This is a warning message.")

# Error Message Box
def show_error_message():
    messagebox.showerror("Error", "This is an error message.")

# Confirmation Message Box
def show_confirmation_message():
    response = messagebox.askyesno("Confirmation", "Are you sure you want to proceed?")
    if response:
        print("User confirmed action.")
    else:
        print("User canceled action.")

# Start the login window
login_window()
