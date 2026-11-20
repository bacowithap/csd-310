# Francisco Villa                   11/20/2026
# Database Development and Use      Module 6.2

""" import statements """
import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values

# Load credentials from .env file
secrets = dotenv_values(".env")

# Database config object
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": secrets["RAISE_ON_WARNINGS"] == True
}

db = None

try:
    # Connect to the movies database
    db = mysql.connector.connect(**config)
    print("\nDatabase user {} connected to MySQL on host {} with database {}".format(
        config["user"], config["host"], config["database"]
    ))

    # Create a cursor object to execute queries
    cursor = db.cursor()

    # 1. Select all fields for the STUDIO table
    print("\n--- DISPLAYING STUDIO RECORDS ---")
    cursor.execute("SELECT studio_id, studio_name FROM studio")
    for studio in cursor.fetchall():
        print(f"Studio ID: {studio[0]}\nStudio Name: {studio[1]}\n")

    # 2. Select all fields for the GENRE table
    print("--- DISPLAYING GENRE RECORDS ---")
    cursor.execute("SELECT genre_id, genre_name FROM genre")
    for genre in cursor.fetchall():
        print(f"Genre ID: {genre[0]}\nGenre Name: {genre[1]}\n")

    # 3. Select movie names with a run time of less than two hours (120 minutes)
    print("--- DISPLAYING SHORT FILM RECORDS ---")
    cursor.execute("SELECT film_name FROM film WHERE film_runtime < 120")
    for film in cursor.fetchall():
        print(f"Film Name: {film[0]}")

    # 4. List of film names and directors ordered by director
    print("--- DISPLAYING DIRECTOR RECORDS IN ORDER ---")
    cursor.execute("SELECT film_name, film_director FROM film ORDER BY film_director")
    for film in cursor.fetchall():
        print(f"Film Name: {film[0]}\nDirector: {film[1]}\n")

    # Close the cursor
    cursor.close()

    input("\nPress Enter to continue...")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist")
    else:
        print(err)

finally:
    # Only close the connection if it was successfully opened
    if db is not None and db.is_connected():
        db.close()
        print("MySQL connection closed.")
