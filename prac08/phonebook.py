from connect import get_connection

def add_user():
    name = input("Enter Name: ")
    phone = input("Enter Phone: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()
    conn.close()
    print("Success!")

def find():
    ptrn = input("Search for: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM find_contacts(%s)", (ptrn,))
    results = cur.fetchall()
    for r in results: 
        print(f"{r[0]}: {r[1]}")
    conn.close()

def add_bulk():
    names = ['Ramazan', 'Bekzat']
    phones = ['87071112233', '87475556677']
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL insert_many(%s, %s)", (names, phones))
    conn.commit()
    conn.close()
    print("Bulk operation finished.")

def pagination():
    limit = int(input("Limit (how many): "))
    offset = int(input("Offset (skip how many): "))
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_paged(%s, %s)", (limit, offset))
    results = cur.fetchall()
    for r in results: 
        print(f"{r[0]}: {r[1]}")
    conn.close()

def delete():
    val = input("Enter Name or Phone to delete: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL delete_contact(%s)", (val,))
    conn.commit()
    conn.close()
    print("Deleted.")

def main():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Add/Update | 2. Find | 3. Bulk Add | 4. Pages | 5. Delete | 0. Exit")
        choice = input("Select action: ")
        if choice == "1": add_user()
        elif choice == "2": find()
        elif choice == "3": add_bulk()
        elif choice == "4": pagination()
        elif choice == "5": delete()
        elif choice == "0": break

if __name__ == "__main__":
    main()