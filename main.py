from flask import Flask, render_template, request, redirect, session, send_file
import user_management as dbHandler
from flask_bcrypt import Bcrypt 
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect
from waitress import serve
from urllib.parse import urlparse, urljoin
import os


# Code snippet for logging a message
# app.logger.critical("message")

app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv("FLASK_SECRET_KEY")
print(app.secret_key)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

#---------------------------------------------------------------------
# Function for checking URLs 
#---------------------------------------------------------------------
def is_safe_url(target): # Checks if given URL is safe to redicrect to 
    host_url = urlparse(request.host_url) # Websites base URL
    redirect_url = urlparse(urljoin(request.host_url, target)) # Combinds the app URL with the user provided URL

    return redirect_url.scheme in ("http", "https") and host_url.netloc == redirect_url.netloc # Returns True and False, only allowing web URLs (Blocking javascript attacks etc . .) and ensures the desination is the same domain as the app
#---------------------------------------------------------------------                           



#---------------------------------------------------------------------
# Function for feedback
#---------------------------------------------------------------------
@app.route("/success.html", methods=["POST", "GET"])
def addFeedback():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")

        if is_safe_url(url): 
            return redirect(url, code=302)
        else:
            return redirect("/")

    if request.method == "POST":
        feedback = request.form["feedback"]
        dbHandler.insertFeedback(feedback)
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")
    else:
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")
#---------------------------------------------------------------------



#---------------------------------------------------------------------
# Function for signup
#---------------------------------------------------------------------
@app.route("/signup.html", methods=["POST", "GET"])
def signup():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "") 

        if is_safe_url(url): 
            return redirect(url, code=302)
        else:
            return redirect("/")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
#------------------------------------------------------------------------------------------------>
# Hashing Passwords
#------------------------------------------------------------------------------------------------>
        hash = bcrypt.generate_password_hash(password).decode('utf-8')
        DoB = request.form["dob"]
        dbHandler.insertUser(username, hash, DoB)
        return render_template("/index.html")
    else:
        return render_template("/signup.html")
#---------------------------------------------------------------------



#---------------------------------------------------------------------
# Function for homepage
#---------------------------------------------------------------------
@app.route("/index.html", methods=["POST", "GET"])
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        
        if is_safe_url(url): 
            return redirect(url, code=302)
        else:
            return redirect("/")

    if request.method == "POST":
        username = request.form["username"]
        password_attempted = request.form["password"]
        isLoggedIn = dbHandler.retrieveUsers(username, password_attempted)
        if isLoggedIn:
            dbHandler.listFeedback()
            return render_template("/success.html", value=username, state=isLoggedIn)
        else:
            return render_template("/index.html")
    else:
        return render_template("/index.html")
#---------------------------------------------------------------------



#---------------------------------------------------------------------
# CSRF TOKENS
#---------------------------------------------------------------------
@app.route('/csrf_test')
def csrf_test():
    return f"Token: {csrf.generate_csrf()}"
#---------------------------------------------------------------------

if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(debug=True, host="0.0.0.0", port=5000)
