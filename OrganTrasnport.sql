CREATE DATABASE OrganTransport;
GO

USE OrganTransport;
GO
DROP TABLE Patients;
DROP TABLE Donors;

CREATE TABLE Patients(
PatientID INT IDENTITY(1,1) PRIMARY KEY,
PatientName VARCHAR(100),
BloodGroup VARCHAR(10),
OrganNeeded VARCHAR(50),
Hospital VARCHAR(100),
Status VARCHAR(50) DEFAULT 'Pending'
);
ALTER TABLE Patients
ADD TrackingStarted INT DEFAULT 0;

CREATE TABLE Donors(
DonorID INT IDENTITY(1,1) PRIMARY KEY,
DonorName VARCHAR(100),
BloodGroup VARCHAR(10),
OrganAvailable VARCHAR(50),
Hospital VARCHAR(100),
Availability VARCHAR(20)
);

INSERT INTO Donors VALUES
('Raj','O+','Heart','Apollo Hospital','Available');

INSERT INTO Patients
(PatientName,BloodGroup,OrganNeeded,Hospital)
VALUES
('Kumar','O+','Heart','Global Hospital');

ALTER TABLE Donors
ADD Latitude FLOAT,
Longitude FLOAT;

INSERT INTO Donors
(DonorName,BloodGroup,OrganAvailable,Hospital,Availability,Latitude,Longitude)
VALUES
('Arun','O+','Heart','Apollo Hospital','Available',13.0827,80.2707);

USE OrganTransport;

ALTER TABLE Patients
ADD Latitude FLOAT,
Longitude FLOAT;

INSERT INTO Patients
(PatientName,BloodGroup,OrganNeeded,Hospital,Latitude,Longitude)
VALUES
('Kumar','O+','Heart','Global Hospital',12.9172,80.2016);

INSERT INTO Donors
(DonorName,BloodGroup,OrganAvailable,Hospital,Availability,Latitude,Longitude)
VALUES
('Arun','O+','Heart','Apollo Hospital','Available',13.0827,80.2707);

select * from Donors;
select * from Patients;

