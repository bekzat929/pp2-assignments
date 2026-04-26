import csv
import os
import json
from connect import get_connection


# ---------------- CREATE TABLES ----------------
def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS groups (
        id SERIAL PRIMARY KEY,
        name TEXT UNIQUE
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name TEXT UNIQUE,
        email TEXT,
        birthday DATE,
        group_id INTEGER REFERENCES groups(id),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS phones (
        id SERIAL PRIMARY KEY,
        contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
        phone TEXT,
        type TEXT CHECK(type IN ('home','work','mobile'))
    );
    """)

    conn.commit()
    conn.close()


# ---------------- ADD CONTACT ----------------
def add_contact():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group = input("Group(Family/Work/Friend/Other): ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
    row = cur.fetchone()

    if row:
        group_id = row[0]
    else:
        cur.execute(
            "INSERT INTO groups(name) VALUES(%s) RETURNING id",
            (group,)
        )
        group_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO contacts(name,email,birthday,group_id)
        VALUES(%s,%s,%s,%s)
        ON CONFLICT(name) DO NOTHING
    """, (name, email, birthday, group_id))

    conn.commit()

    cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
    contact_id = cur.fetchone()[0]

    while True:
        phone = input("Phone (empty to stop): ")
        if phone == "":
            break

        ptype = input("Type(home/work/mobile): ")

        cur.execute("""
            INSERT INTO phones(contact_id, phone, type)
            VALUES(%s,%s,%s)
        """, (contact_id, phone, ptype))

        conn.commit()

    print("Contact added successfully!")
    conn.close()


# ---------------- CSV IMPORT ----------------
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
            # name,email,birthday,group,phone,type
            name, email, birthday, group, phone, ptype = row

            cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
            data = cur.fetchone()

            if data:
                gid = data[0]
            else:
                cur.execute(
                    "INSERT INTO groups(name) VALUES(%s) RETURNING id",
                    (group,)
                )
                gid = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO contacts(name,email,birthday,group_id)
                VALUES(%s,%s,%s,%s)
                ON CONFLICT(name) DO NOTHING
            """, (name, email, birthday, gid))

            cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
            cid = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO phones(contact_id,phone,type)
                VALUES(%s,%s,%s)
            """, (cid, phone, ptype))

    conn.commit()
    print("CSV Imported!")
    conn.close()


# ---------------- SHOW CONTACTS ----------------
def show_all():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT c.name,c.email,c.birthday,g.name,p.phone,p.type
    FROM contacts c
    LEFT JOIN groups g ON c.group_id=g.id
    LEFT JOIN phones p ON c.id=p.contact_id
    ORDER BY c.name
    """)

    rows = cur.fetchall()

    if not rows:
        print("No contacts found.")
    else:
        for row in rows:
            print(row)

    conn.close()

# ---------------- SEARCH ----------------
def find():
    search = input("Search name/email/phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT c.name,c.email,p.phone
    FROM contacts c
    LEFT JOIN phones p ON c.id=p.contact_id
    WHERE c.name ILIKE %s
       OR c.email ILIKE %s
       OR p.phone ILIKE %s
    """, (f'%{search}%', f'%{search}%', f'%{search}%'))

    rows = cur.fetchall()

    for row in rows:
        print(row)

    conn.close()


# ---------------- FILTER GROUP ----------------
def filter_group():
    group = input("Group name: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT c.name,c.email
    FROM contacts c
    JOIN groups g ON c.group_id=g.id
    WHERE g.name=%s
    """, (group,))

    for row in cur.fetchall():
        print(row)

    conn.close()


# ---------------- DELETE ----------------
def delete():
    name = input("Contact name to delete: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM contacts WHERE name=%s", (name,))
    conn.commit()

    conn.close()


# ---------------- EXPORT JSON ----------------
def export_json():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT c.name,c.email,c.birthday,g.name
    FROM contacts c
    LEFT JOIN groups g ON c.group_id=g.id
    """)

    rows = cur.fetchall()
    data = []

    for row in rows:
        data.append({
            "name": row[0],
            "email": row[1],
            "birthday": str(row[2]),
            "group": row[3]
        })

    with open("contacts.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Exported to contacts.json")
    conn.close()


# ---------------- IMPORT JSON ----------------
def import_json():
    if not os.path.exists("contacts.json"):
        print("contacts.json not found")
        return

    conn = get_connection()
    cur = conn.cursor()

    with open("contacts.json") as f:
        data = json.load(f)

    for item in data:
        cur.execute("""
        INSERT INTO contacts(name,email,birthday)
        VALUES(%s,%s,%s)
        ON CONFLICT(name) DO NOTHING
        """, (
            item["name"],
            item["email"],
            item["birthday"]
        ))

    conn.commit()
    print("Imported JSON")
    conn.close()


# ---------------- MAIN MENU ----------------
def main():
    create_tables()

    while True:
        print("""
1. CSV Import
2. Add Contact
3. Show All
4. Search
5. Filter Group
6. Delete
7. Export JSON
8. Import JSON
0. Exit
""")

        choice = input("Action: ")

        if choice == "1":
            upload_csv()
        elif choice == "2":
            add_contact()
        elif choice == "3":
            show_all()
        elif choice == "4":
            find()
        elif choice == "5":
            filter_group()
        elif choice == "6":
            delete()
        elif choice == "7":
            export_json()
        elif choice == "8":
            import_json()
        elif choice == "0":
            break


if __name__ == "__main__":
    main()