from flask import Flask, jsonify, render_template, request, redirect
import json
import pymongo
from pymongo.errors import PyMongoError

app = Flask(__name__)

# ---------- MongoDB Atlas connection ----------
# Put your own connection string here
MONGO_URI = "mongodb+srv://vijayrgaligali_db_user:UhYLNFRP3j09KjP8@student.d8zmsx1.mongodb.net/"

try:
    client = pymongo.MongoClient(MONGO_URI)
    db = client["flaskdb"]          # your database name
    collection = db["students"]     # your collection name
    print("Connected to MongoDB Atlas successfully")
except PyMongoError as e:
    print("Error connecting to MongoDB:", e)
    client = None
    db = None
    collection = None

# ---------- /api route: returns JSON list from backend file ----------
@app.route("/api")
def api_route():
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        # If anything goes wrong reading the file
        return jsonify({"error": str(e)}), 500

# ---------- Frontend form ----------
@app.route("/", methods=["GET", "POST"])
def form():
    error_message = None

    if request.method == "POST":
        if collection is None:
            error_message = "Database connection not available."
            return render_template("form.html", error=error_message)

        # Get data from form
        name = request.form.get("name")
        email = request.form.get("email")

        # Simple validation
        if not name or not email:
            error_message = "Please fill in all fields."
            return render_template("form.html", error=error_message)

        # Document to insert in MongoDB
        doc = {
            "name": name,
            "email": email
        }

        # Try to insert into MongoDB
        try:
            collection.insert_one(doc)
            # On success, redirect to success page
            return redirect("/success")
        except PyMongoError as e:
            # On error, stay on same page and show error
            error_message = f"Error inserting into database: {e}"
            return render_template("form.html", error=error_message)

    # GET request: just show form
    return render_template("form.html", error=error_message)

# ---------- Success page ----------
@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)