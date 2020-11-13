import pyodbc

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\jinye\work\fyp\LinkBudget\95500106_20201111.mdb;')
cursor = conn.cursor()
cursor.execute('select * from emiss')
   
for row in cursor.fetchall():
    print (row)