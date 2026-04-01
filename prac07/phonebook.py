import csv
import os
from connect import get_connection

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS phonebook (name TEXT, phone TEXT);")
    conn.commit()
    cur.close()
    conn.close()

def upload_csv():
    filename = input("CSV file name: ")
    if not os.path.exists(filename):
        print("File not found!")
        return
    conn = get_connection()
    cur = conn.cursor()
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (row[0], row[1]))
    conn.commit()
    print("Done!")
    conn.close()

def add_contact():
    name = input("Name: ")
    phone = input("Phone: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    conn.close()

def update_contact():
    target = input("Contact name to update: ")
    new_phone = input("New phone: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE phonebook SET phone = %s WHERE name = %s", (new_phone, target))
    conn.commit()
    conn.close()

def find():
    search = input("Search (name or prefix): ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook WHERE name ILIKE %s OR phone LIKE %s", (f'%{search}%', f'{search}%'))
    rows = cur.fetchall()
    for row in rows:
        print(f"{row[0]}: {row[1]}")
    conn.close()

def delete():
    val = input("Name or phone to delete: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM phonebook WHERE name = %s OR phone = %s", (val, val))
    conn.commit()
    conn.close()

def main():
    create_table()
    while True:
        print("\n1. CSV | 2. Add | 3. Update | 4. Find | 5. Delete | 0. Exit")
        choice = input("Action: ")
        if choice == "1": upload_csv()
        elif choice == "2": add_contact()
        elif choice == "3": update_contact()
        elif choice == "4": find()
        elif choice == "5": delete()
        elif choice == "0": break

if __name__ == "__main__":
    main()