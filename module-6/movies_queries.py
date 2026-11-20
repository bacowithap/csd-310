# Francisco Villa                   11/20/2026
# Database Development and Use      Module 6.2

""" import statements """
import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values, find_dotenv

# Load credentials from .env file
secrets = dotenv_values(find_dotenv())

# Database config object
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": secrets["RAISE_ON_WARNINGS"] == "True"
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

    # 1. Select all fields for the studio table
    print("\n-- DISPLAYING Studio RECORDS --")
    cursor.execute("SELECT studio_id, studio_name FROM studio")
    for studio in cursor.fetchall():
        print(f"Studio ID: {studio[0]}\nStudio Name: {studio[1]}\n")

    # 2. Select all fields for the genre table
    print("\n-- DISPLAYING Genre RECORDS --")
    cursor.execute("SELECT genre_id, genre_name FROM genre")
    for genre in cursor.fetchall():
        print(f"Genre ID: {genre[0]}\nGenre Name: {genre[1]}\n")

    # 3. Select movie names with a run time of less than two hours
    print("\n-- DISPLAYING Short Film RECORDS --")
    cursor.execute("SELECT film_name, film_runtime FROM film WHERE film_runtime < 120")
    for film in cursor.fetchall():
        print(f"Film Name: {film[0]}\nRuntime: {film[1]}\n")

    # 4. List of film names and directors ordered by director
    print("\n-- DISPLAYING Director RECORDS in Order --")
    cursor.execute("SELECT film_name, film_director FROM film ORDER BY film_director")
    for film in cursor.fetchall():
        print(f"Film Name: {film[0]}\nDirector: {film[1]}\n")

    # Close the cursor
    cursor.close()

    input("\nPress any key to continue...")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist")
    else:
        print(err)

finally:
    if db is not None and db.is_connected():
        db.close()
