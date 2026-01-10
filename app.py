print("🔥🔥🔥 NEW BACKEND STARTED 🔥🔥🔥")

from flask import Flask, request, jsonify, render_template

from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os
app = Flask(__name__)
CORS(app)

# -----------------------------
# FIREBASE SETUP
# -----------------------------
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# -----------------------------
# TEST ROUTE
# -----------------------------
@app.route("/", methods=["GET"])
def home():
    return "CityPulse Backend is Running ✅"

# -----------------------------
# CREATE ISSUE (USER)
# -----------------------------
# -----------------------------
# FRONTEND ROUTES
# -----------------------------

@app.route("/admin")
def admin_dashboard():
    return render_template("admin-dashboard.html")

@app.route("/user")
def user_dashboard():
    return render_template("user-dashboard.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/home")
def home_page():
    return render_template("index.html")
@app.route("/report", methods=["POST"])
def report_issue():
    data = request.json

    issue = {
        "issueType": data.get("issueType"),
        "location": data.get("location"),
        "description": data.get("description"),
        "imageUrl": data.get("imageUrl"),  # 🔥 STORE URL
        "status": "pending",
        "createdAt": datetime.now()
    }

    db.collection("issues").add(issue)
    return jsonify({"message": "Issue reported successfully"}), 201

# -----------------------------
# GET ALL ISSUES (ADMIN)
# -----------------------------
@app.route("/issues", methods=["GET"])
def get_issues():
    issues_ref = db.collection("issues").stream()
    issues = []

    for issue in issues_ref:
        temp = issue.to_dict()
        temp["id"] = issue.id
        issues.append(temp)

    return jsonify(issues)

# -----------------------------
# UPDATE ISSUE STATUS (ADMIN)
# -----------------------------


@app.route("/update/<issue_id>", methods=["POST"])
def update_status(issue_id):
    data = request.json
    new_status = data.get("status")

    print("UPDATE CALLED ->", issue_id, new_status)

    if not new_status:
        return jsonify({"error": "Status missing"}), 400

    db.collection("issues").document(issue_id).update({
        "status": new_status
    })

    return jsonify({"message": "Status updated"})

# -----------------------------
# RUN SERVER
# -----------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


