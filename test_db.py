import pyodbc

print("Testing SQL Server connection...")

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=SARAS\SQLEXPRESS01;"
    "DATABASE=OrganTransport;"
    "Trusted_Connection=yes;"
)

print("✅ Database Connected Successfully")

cursor = conn.cursor()
cursor.execute("SELECT name FROM sys.tables")

for row in cursor:
    print(row)

conn.close()