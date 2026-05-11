import sqlite3

conn = sqlite3.connect('chinook.db')
cursor = conn.cursor()


def add_artist(New_artist):
    try:
        cursor.execute("INSERT INTO artists (Name) VALUES (?)", (New_artist,))
        conn.commit()
        print("Artist added. ID:", cursor.lastrowid)
    except sqlite3.Error as e:
        print("Error adding artist:", e)

def update_artist(updated_name, artist_id):
    try:
        cursor.execute("UPDATE artists SET Name = ? WHERE ArtistId = ?", (updated_name, artist_id))
        conn.commit()
        print("Rows updated:", cursor.rowcount)
    except sqlite3.Error as e:
        print("Error updating artist:", e)

def delete_artist(artist_id):
    try:
        cursor.execute("DELETE FROM artists WHERE ArtistId = ?", (artist_id,))
        conn.commit()
        print("Rows deleted:", cursor.rowcount)
    except sqlite3.Error as e:
        print("Error deleting artist:", e)


while True:
    print("Choose an option:")
    print("1. Add Artist")
    print("2. Update Artist")
    print("3. Delete Artist")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        new_artist = input("Enter Artist Name: ")
        add_artist(new_artist)
    elif choice == "2":
        updated_name = input("Enter Updated Artist Name: ")
        artist_id = int(input("Enter Artist ID to Update: "))
        update_artist(updated_name, artist_id)
    elif choice == "3":
        artist_id = int(input("Enter Artist ID to Delete: "))
        delete_artist(artist_id)
    elif choice == "4":
        break
    else:
        print("Invalid choice. Please try again.")



conn.close()