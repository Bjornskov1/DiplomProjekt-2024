import csv
import mysql.connector

# Database connection configuration
config = {
    'user': '379731_mabj',
    'password': 'MABJ1337',
    'host': 'mysql-initmeeting.alwaysdata.net',
    'database': 'initmeeting_db',
}

# Path to the CSV file with user data
file_path = r'C:/Users/mag08/OneDrive - Danmarks Tekniske Universitet/Dokumenter/alle_lynge.csv'

# Connect to the database
connection = mysql.connector.connect(**config)
cursor = connection.cursor()


# Function to import users from CSV
def import_users_from_csv(file_path):
    with open(file_path, mode='r', encoding='latin1') as file:
        # Specify the delimiter as a semicolon
        csv_reader = csv.DictReader(file, delimiter=';')

        # Debug: Print header fields to ensure correct mapping
        print("CSV Headers:", csv_reader.fieldnames)

        # Read each row in the CSV
        for row in csv_reader:
            name = row.get('Name')
            email = row.get('Email')

            # Debug: Print row content
            print("Row Data:", row)

            if name and email:
                try:
                    # Insert user into the database
                    cursor.execute(
                        "INSERT INTO my_app_user (name, email) VALUES (%s, %s)",
                        (name, email)
                    )
                    print(f"Inserted user: {name} ({email})")
                except mysql.connector.IntegrityError:
                    print(f"User {name} ({email}) already exists. Skipping.")
            else:
                print("Skipping row due to missing data:", row)

    # Commit the transaction to save changes
    connection.commit()
    print("User import completed.")


# Run the import function
import_users_from_csv(file_path)

# Close the database connection
cursor.close()
connection.close()
