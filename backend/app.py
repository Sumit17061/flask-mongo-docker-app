import json
import os
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev")

# MongoDB setup
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "flask_assignment")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "submissions")

client = MongoClient(MONGODB_URI) if MONGODB_URI else None
db = client[DB_NAME] if client else None
collection = db[COLLECTION_NAME]


def read_backend_data():
    with open("data.json", "r") as f:
        return json.load(f)


@app.route("/api", methods=["GET"])
def api():
    data = read_backend_data()
    return jsonify(data), 200


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        # Basic validation
        if not name or not email or not message:
            flash("All fields are required.", "error")
            return render_template("index.html")

        if collection is None:
            flash("MongoDB is not configured.", "error")
            return render_template("index.html")


        try:
            collection.insert_one({"name": name, "email": email, "message": message})
            return redirect(url_for("success"))
        except Exception as e:
            flash(f"Error while inserting into MongoDB: {e}", "error")
            return render_template("index.html")

    return render_template("index.html")


@app.route("/success")
def success():
    return render_template("success.html", msg="Data submitted successfully")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)


