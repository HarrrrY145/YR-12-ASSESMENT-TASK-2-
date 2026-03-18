import sqlite3 as sql
import time
import random

# Inserting Users into a database
def insertUser(username, password, DoB):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()


#This is SQL injection proof. 
    cur.execute("INSERT INTO users (username,password,dateOfBirth) VALUES (?,?,?)", (username, password, DoB),)
    con.commit()
    con.close()

#CHECK FOR FILE SAFTEY 
def retrieveUsers(username, password):
    con = sql.connect("database_files/database.db") #Connecting to database
    cur = con.cursor() 

    cur.execute("SELECT * FROM users WHERE username == ?", (username)) # Selecting the username from database
    if cur.fetchone() == None: # If no username is found in the database
        con.close() # Close database
        return False 

    else: # If a username is found in the database
        cur.execute("SELECT * FROM users WHERE password == ?", (password)) # Select the password from the database
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
        if cur.fetchone() == None:
            con.close()
            return False
        else:
            con.close()
            return True

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
        f.write(f"{row[1]}\n") # Write feedback
        f.write("</p>\n") # New line
    f.close() # Close file