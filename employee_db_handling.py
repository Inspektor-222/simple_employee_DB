import sqlite3
from employee_class import Employee
from pathlib import Path

# conn = sqlite3.connect(':memory:')
conn = sqlite3.connect(Path(r"employee_db.db"))
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first TEXT,
            last TEXT,
            pay INTEGER
            )""")

def insert_emp(emp):
    conn = sqlite3.connect(Path(r"employee_db.db"))
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO employees (first, last, pay) VALUES (:first, :last, :pay)", {'first': emp.first, 'last': emp.last, 'pay': emp.pay})

def get_emps_by_name(lastname):
    conn = sqlite3.connect(Path(r"employee_db.db"))
    c = conn.cursor()
    with conn:
        c.execute("SELECT * FROM employees WHERE last=:last", {'last': lastname})
    return c.fetchall()

def get_all_emps():
    conn = sqlite3.connect(Path(r"employee_db.db"))
    c = conn.cursor()
    with conn:
        c.execute("SELECT * FROM employees")
    return c.fetchall()

def update_pay(emp, pay):
    conn = sqlite3.connect(Path(r"employee_db.db"))
    c = conn.cursor()
    with conn:
        c.execute("""UPDATE employees SET pay = :pay
                    WHERE first = :first AND last = :last""",
                  {'first': emp.first, 'last': emp.last, 'pay': pay})

def update_data(emp):
    id, firstname, lastname, pay = emp
    conn = sqlite3.connect(Path(r"employee_db.db"))
    c = conn.cursor()
    with conn:
        c.execute("""UPDATE employees SET first = :first, last = :last, pay = :pay
                    WHERE id = :id""",
                  {'id': id, 'first': firstname ,'last': lastname, 'pay': pay})

def remove_emp(id):
    conn = sqlite3.connect(Path(r"employee_db.db"))
    c = conn.cursor()
    with conn:
        c.execute("DELETE from employees WHERE id = :id", {'id': id})

# emp_1 = Employee('John', 'Doe', 80000)
# emp_2 = Employee('Jane', 'Doe', 90000)
# emp_3 = Employee()
# emp_3.first = 'Manuel'
# emp_3.last = 'Gräfe'
# emp_3.pay = 4500

# insert_emp(emp_1)
# insert_emp(emp_2)
# insert_emp(emp_3)

# emps = get_emps_by_name('Schafer')
# print(emps)

# update_pay(emp_2, 95000)
# remove_emp(emp_1)

# emps = get_emps_by_name('Doe')
# print(emps)

conn.close()
