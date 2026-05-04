from flask import Flask, render_template, request, jsonify, redirect, session
import pyodbc
from blockchain import organ_chain
app = Flask(__name__)
app.secret_key = "organ_transport_secret"

# -----------------------------------
# HOSPITAL COORDINATES
# -----------------------------------

hospitals = {
    "Apollo Hospital": (13.0827, 80.2707),
    "Global Hospital": (12.9172, 80.2016),
    "MIOT Hospital": (13.0418, 80.1913),
    "Fortis Hospital": (13.0527, 80.2123)
}

# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------

def get_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "Server=SARAS\\SQLEXPRESS01;"
        "DATABASE=OrganTransport;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
    return conn

# -----------------------------------
# HOME PAGE
# -----------------------------------

@app.route("/")
def home():
    return redirect("/login")

# -----------------------------------
# ADMIN LOGIN
# -----------------------------------

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            session["admin"] = True
            return redirect("/dashboard")
        else:
            return "Invalid Login"

    return render_template("login.html")


# -----------------------------------
# LOGOUT
# -----------------------------------

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/login")

# -----------------------------------
# ADMIN DASHBOARD
# -----------------------------------

@app.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Patients")
    patients = cursor.fetchall()

    return render_template("dashboard.html", patients=patients)

# -----------------------------------
# PATIENT REQUEST PAGE
# -----------------------------------

@app.route("/request")
def request_page():
    return render_template("request.html")

# -----------------------------------
# ADD PATIENT
# -----------------------------------

@app.route("/add_patient", methods=["POST"])
def add_patient():

    name = request.form["name"]
    blood = request.form["blood"]
    organ = request.form["organ"]
    hospital = request.form["hospital"]

    lat, lon = hospitals[hospital]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO Patients
    (PatientName, BloodGroup, OrganNeeded, Hospital, Latitude, Longitude, Status)
    VALUES (?,?,?,?,?,?,?)
    """, (name, blood, organ, hospital, lat, lon, "Pending"))

    conn.commit()

    return render_template("request_success.html")

# -----------------------------------
# ADD DONOR
# -----------------------------------

@app.route("/add_donor", methods=["POST"])
def add_donor():

    name = request.form["name"]
    blood = request.form["blood"]
    organ = request.form["organ"]
    hospital = request.form["hospital"]
    availability = request.form["availability"]

    lat, lon = hospitals[hospital]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO Donors
    (DonorName,BloodGroup,OrganAvailable,Hospital,Availability,Latitude,Longitude)
    VALUES (?,?,?,?,?,?,?)
    """,(name,blood,organ,hospital,availability,lat,lon))

    conn.commit()

    return redirect("/donors")
# -----------------------------------
# APPROVE PATIENT
# -----------------------------------
@app.route("/approve/<id>", methods=["POST"])
def approve(id):

    if "admin" not in session:
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    # Get patient
    cursor.execute("SELECT * FROM Patients WHERE PatientID=?", (id,))
    patient = cursor.fetchone()

    if not patient:
        return jsonify({"status":"Patient Not Found"})

    blood = patient.BloodGroup
    organ = patient.OrganNeeded

    # Find available donor
    cursor.execute("""
    SELECT TOP 1 * FROM Donors
    WHERE BloodGroup=?
    AND OrganAvailable=?
    AND Availability='Available'
    """,(blood,organ))

    donor = cursor.fetchone()

    if donor:

        # Approve patient
        cursor.execute("""
        UPDATE Patients
        SET Status='Approved'
        WHERE PatientID=?
        """,(id,))

        # Make donor unavailable
        cursor.execute("""
        UPDATE Donors
        SET Availability='Unavailable'
        WHERE DonorID=?
        """,(donor.DonorID,))

        conn.commit()

        return jsonify({"status":"Approved & Donor Assigned"})

    else:

        cursor.execute("""
        UPDATE Patients
        SET Status='Rejected'
        WHERE PatientID=?
        """,(id,))

        conn.commit()

        return jsonify({"status":"No Donor Available"})
@app.route("/start_tracking/<id>")
def start_tracking(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT TrackingStarted, Status FROM Patients WHERE PatientID=?", (id,))
    patient = cursor.fetchone()

    if patient.Status == "Arrived":
        return jsonify({"status":"arrived"})

    if patient.TrackingStarted == 1:
        return jsonify({"status":"arrived"})

    cursor.execute("""
    UPDATE Patients
    SET TrackingStarted=1
    WHERE PatientID=?
    """,(id,))

    conn.commit()
    organ_chain.add_block("Patient Approved ID: " + str(id))

    return jsonify({"status":"started"})
# -----------------------------------
# VIEW DONORS
# -----------------------------------

@app.route("/donors")
def donors():

    if "admin" not in session:
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Donors")
    donors = cursor.fetchall()

    return render_template("donors.html", donors=donors)

# -----------------------------------
# AMBULANCE MAP
# -----------------------------------

@app.route("/map/<id>")
def map_page(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Patients WHERE PatientID=?", (id,))
    patient = cursor.fetchone()

    cursor.execute("""
    SELECT TOP 1 * FROM Donors
    WHERE BloodGroup=? 
    AND OrganAvailable=?
    """,(patient.BloodGroup, patient.OrganNeeded))

    donor = cursor.fetchone()

    return render_template("map.html", patient=patient, donor=donor)
@app.route("/mark_arrived/<id>", methods=["POST"])
def mark_arrived(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE Patients
    SET Status='Arrived'
    WHERE PatientID=?
    """,(id,))

    conn.commit()
    
    organ_chain.add_block("Organ Delivered to Patient ID: " + str(id))
    return jsonify({"status":"updated"})

@app.route("/blockchain")
def view_blockchain():

    data = []

    for block in organ_chain.chain:
        data.append({
            "data": block.data,
            "hash": block.hash,
            "prev": block.previous_hash
        })

    return render_template("blockchain.html", chain=data)
# -----------------------------------
# RUN SERVER
# -----------------------------------

if __name__ == "__main__":
    app.run(debug=True)