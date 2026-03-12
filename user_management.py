import sqlite3 as sql
import time
import random

# Inserting Users into a database
def insertUser(username, password, DoB):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(

#CHECK FOR SQL INJECTION
        "INSERT INTO users (username,password,dateOfBirth) VALUES (?,?,?)",
        (username, password, DoB),)
    con.commit()
    con.close()

#CHECK FOR FILE SAFTEY 
def retrieveUsers(username, password):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM users WHERE username = '{username}'")
    if cur.fetchone() == None:
        con.close()
        return False
    else:
        cur.execute(f"SELECT * FROM users WHERE password = '{password}'")
        # Plain text log of visitor count as requested by Unsecure PWA management
        with open("visitor_log.txt", "r") as file:
            number = int(file.read().strip())
            number += 1
        with open("visitor_log.txt", "w") as file:
            file.write(str(number))
        # Simulate response time of heavy app for testing purposes
        time.sleep(random.randint(80, 90) / 1000)
        if cur.fetchone() == None:
            con.close()
            return False
        else:
            con.close()
            return True

# Inserting feedback into a database
def insertFeedback(feedback):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()

#CHECK FOR SQL INJECTION
    cur.execute("INSERT INTO feedback (feedback) VALUES (?)", (feedback,)) # Removing the F-string and implementimg query parameters to prevent SQL injections.
    con.commit()
    con.close()

#CHECK FOR FILE SAFTEY 
def listFeedback():
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM feedback").fetchall()
    con.close()
    f = open("templates/partials/success_feedback.html", "w")
    for row in data:
        f.write("<p>\n")
        f.write(f"{row[1]}\n")
        f.write("</p>\n")
    f.close()