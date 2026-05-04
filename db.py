import pyodbc

def get_connection():
    conn = pyodbc.connect(
 "DRIVER={ODBC Driver 18 for SQL Server};"       
 "Server=SARAS\SQLEXPRESS01;"  # replace with your SQL Server
        "Database=OrganTransport;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes"
    )
    return conn