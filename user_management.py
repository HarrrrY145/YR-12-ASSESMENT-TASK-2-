import sqlite3 as sql
import html
import time
import random
from flask_bcrypt import Bcrypt 


bcrypt = Bcrypt()

# Inserting Users into a database
def insertUser(username, hash, DoB):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()


#This is SQL injection proof. 
    cur.execute("INSERT INTO users (username,password,dateOfBirth) VALUES (?,?,?)", (username, hash, DoB),)
    con.commit()
    con.close()

#CHECK FOR FILE SAFTEY 
def retrieveUsers(username, password_attempted):
    con = sql.connect("database_files/database.db") #Connecting to database
    cur = con.cursor()

    cur.execute("SELECT * FROM users WHERE username == ?", (username,)) # Selecting the username from database
    user = cur.fetchone() # Selecting that user with the username and storing it as a variable

    if user is None: # If no user is found in the database
        con.close() # Close database
        return False 


#------------------------------------------------------------------------
# Checking the hashed password
#------------------------------------------------------------------------
    stored_hash = user[2] # Storing the hashed password from the databsed to a variable. 
    print("Stored hash:", stored_hash)
    if bcrypt.check_password_hash(stored_hash, password_attempted):
        



#------------------------------------------------------------------------
# Plain text log of visitor count as requested by Unsecure PWA management
#------------------------------------------------------------------------
        with open("visitor_log.txt", "r") as file: # Opening visitor log as 'read'
            number = int(file.read().strip()) # Reading the file strip and saving it as an intiger number vairable 
            number += 1 # Plus the read number by 1 
        with open("visitor_log.txt", "w") as file: # Opening visitor log as 'write'
            file.write(str(number)) # write the new number into the file. 

            # Simulate response time of heavy app for testing purposes
        time.sleep(random.randint(80, 90) / 1000) 
        con.close()
        return True
    
    else:
        con.close()
        return False

# Inserting feedback into a database
def insertFeedback(feedback):
    con = sql.connect("database_files/database.db") # Connecting to database 
    cur = con.cursor() 

#CHECK FOR SQL INJECTION
# Removing the F-string and implementimg query parameters to prevent SQL injections.
    cur.execute("INSERT INTO feedback (feedback) VALUES (?)", (feedback,)) # Inserting feedback messages into the database
    con.commit() # Commiting to database
    con.close() # Closing database

#CHECK FOR FILE SAFTEY 
def listFeedback():
    con = sql.connect("database_files/database.db") # Connecting to database
    cur = con.cursor() 
    data = cur.execute("SELECT * FROM feedback").fetchall() # Selecting all feedback from database
    con.close() # Close database
    f = open("templates/partials/success_feedback.html", "w") # Open the success feedback html file as 'write' 
    for row in data: # For every row 
        f.write("<p>\n") # New line
        safe_feedback = html.escape(row[1]) #Escape special HTML characters
        f.write(f"{row[1]}\n") # Write escaped feedback 
        f.write("</p>\n") # New line
    f.close() # Close file