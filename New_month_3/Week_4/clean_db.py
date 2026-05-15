import sqlite3


try:
    conn = sqlite3.connect('titanic.db')
    cursor = conn.cursor()
except Exception as e:
    print(f"An error occured connecting database {e} ")

def fix_age():
    try:
        cursor.execute("SELECT AVG(age) FROM passengers WHERE age is not NULL")
        avg_age = cursor.fetchone()[0]
        cursor.execute("UPDATE passengers SET age = ? WHERE age IS NULL", (avg_age,))
        conn.commit()
    except Exception as e:
        print(f"An error occurred while fixing age: {e}")

def fix_embarked():
    try:
        cursor.execute("UPDATE passengers SET embarked = 'S' WHERE embarked IS NULL")
        conn.commit()
    except Exception as e:
        print(f"An error occurred while fixing embarked: {e}")

def fix_cabin():
    try:
        # Add the column if it doesn't exist
        cursor.execute("ALTER TABLE passengers ADD COLUMN has_cabin INTEGER")
    except sqlite3.OperationalError as e:
        if "duplicate column name" not in str(e):
            raise
    try:
        cursor.execute("UPDATE passengers SET has_cabin = CASE WHEN cabin IS NOT NULL AND cabin != '' THEN 1 ELSE 0 END")
        conn.commit()
    except Exception as e:
        print(f"Error updating has_cabin: {e}")

def extract_title():
    try:
        cursor.execute("ALTER TABLE passengers ADD COLUMN title TEXT")
    except sqlite3.OperationalError as e:
        if "duplicate column name" not in str(e):
            raise
    try:
        cursor.execute("""
            UPDATE passengers SET title = 
                CASE 
                    WHEN name LIKE '%, Mr.%' THEN 'Mr'
                    WHEN name LIKE '%, Mrs.%' THEN 'Mrs'
                    WHEN name LIKE '%, Miss.%' THEN 'Miss'
                    WHEN name LIKE '%, Master.%' THEN 'Master'
                    WHEN name LIKE '%, Dr.%' THEN 'Dr'
                    ELSE 'Other'
                END
        """)
        conn.commit()
    except Exception as e:
        print(f"Error extracting title: {e}")

def main():
    fix_age()
    fix_embarked()
    fix_cabin()
    extract_title()
    conn.close()

if __name__ == "__main__":    main()

