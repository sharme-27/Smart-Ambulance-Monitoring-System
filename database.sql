CREATE TABLE Patients(
PatientID INT IDENTITY PRIMARY KEY,
PatientName VARCHAR(100),
BloodGroup VARCHAR(10),
OrganNeeded VARCHAR(50),
Hospital VARCHAR(100)
)

CREATE TABLE Donors(
DonorID INT IDENTITY PRIMARY KEY,
DonorName VARCHAR(100),
BloodGroup VARCHAR(10),
OrganType VARCHAR(50),
Hospital VARCHAR(100),
FamilyApproval VARCHAR(20),
Availability VARCHAR(20)
)

CREATE TABLE Transport(
TransportID INT IDENTITY PRIMARY KEY,
DonorID INT,
PatientID INT,
VehicleNo VARCHAR(20),
Status VARCHAR(50)
)

CREATE TABLE LocationData(
LocationID INT IDENTITY PRIMARY KEY,
TransportID INT,
Latitude FLOAT,
Longitude FLOAT,
TimeStamp DATETIME DEFAULT GETDATE()
)