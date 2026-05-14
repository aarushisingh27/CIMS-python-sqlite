import sqlite3
from tabulate import tabulate

# ------------------------------
# DATABASE CONNECTION
# ------------------------------

con = sqlite3.connect("cims.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS students(
    sid INTEGER PRIMARY KEY,
    s_name TEXT,
    pno INTEGER,
    course TEXT,
    joining_date TEXT,
    mode TEXT,
    duration INTEGER,
    city TEXT
)
""")

con.commit()

print("\nDatabase Connected Successfully")

# ------------------------------
# LOGIN SYSTEM
# ------------------------------

username = input("\nEnter Username: ")
password = input("Enter Password: ")

if username.lower() != "admin" or password != "1234":
    print("\nUnauthorized Access")
    exit()

print("\nWelcome To Computer Institute Management System")

# ------------------------------
# FUNCTIONS
# ------------------------------

def add_student():
    print("\nADD STUDENT")

    sid = int(input("Student ID: "))
    name = input("Student Name: ")
    phone = int(input("Phone Number: "))
    course = input("Course Name: ")
    joining_date = input("Joining Date (YYYY-MM-DD): ")
    mode = input("Course Mode (Online/Offline): ")
    duration = int(input("Duration (Months): "))
    city = input("City: ")

    query = """
    INSERT INTO students
    VALUES (?,?,?,?,?,?,?,?)
    """

    values = (
        sid,
        name,
        phone,
        course,
        joining_date,
        mode,
        duration,
        city
    )

    try:
        cur.execute(query, values)
        con.commit()
        print("\nStudent Added Successfully")

    except sqlite3.IntegrityError:
        print("\nStudent ID Already Exists")


def view_students():
    print("\nALL STUDENTS")

    query = "SELECT * FROM students"
    cur.execute(query)

    data = cur.fetchall()

    if len(data) == 0:
        print("\nNo Records Found")
        return

    print(tabulate(
        data,
        headers=[
            "ID",
            "Name",
            "Phone",
            "Course",
            "Joining Date",
            "Mode",
            "Duration",
            "City"
        ],
        tablefmt="fancy_grid"
    ))


def search_student():
    print("\nSEARCH STUDENT")

    sid = int(input("Enter Student ID: "))

    query = "SELECT * FROM students WHERE sid = ?"
    cur.execute(query, (sid,))

    data = cur.fetchone()

    if data:
        print(tabulate(
            [data],
            headers=[
                "ID",
                "Name",
                "Phone",
                "Course",
                "Joining Date",
                "Mode",
                "Duration",
                "City"
            ],
            tablefmt="fancy_grid"
        ))
    else:
        print("\nStudent Not Found")


def update_student():
    print("\nUPDATE STUDENT")

    sid = int(input("Enter Student ID: "))
    phone = int(input("New Phone Number: "))
    mode = input("New Mode: ")
    duration = int(input("New Duration: "))

    query = """
    UPDATE students
    SET pno=?, mode=?, duration=?
    WHERE sid=?
    """

    values = (phone, mode, duration, sid)

    cur.execute(query, values)
    con.commit()

    if cur.rowcount == 0:
        print("\nStudent Not Found")
    else:
        print("\nStudent Updated Successfully")


def delete_student():
    print("\nDELETE STUDENT")

    sid = int(input("Enter Student ID: "))

    query = "DELETE FROM students WHERE sid = ?"
    cur.execute(query, (sid,))

    con.commit()

    if cur.rowcount == 0:
        print("\nStudent Not Found")
    else:
        print("\nStudent Deleted Successfully")


# ------------------------------
# MAIN MENU
# ------------------------------

while True:

    print("\n" + "=" * 60)
    print("COMPUTER INSTITUTE MANAGEMENT SYSTEM")
    print("=" * 60)

    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")

    try:
        choice = int(input("\nEnter Choice: "))

        if choice == 1:
            add_student()

        elif choice == 2:
            view_students()

        elif choice == 3:
            search_student()

        elif choice == 4:
            update_student()

        elif choice == 5:
            delete_student()

        elif choice == 6:
            print("\nThank You For Using CIMS")
            break

        else:
            print("\nInvalid Choice")

    except ValueError:
        print("\nPlease Enter Valid Numeric Input")