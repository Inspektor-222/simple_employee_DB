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


conn.close()
