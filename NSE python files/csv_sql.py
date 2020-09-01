import pandas as pd
# import pyodbc
import mysql.connector

data = pd.read_csv (r'E:\py_docs\cm03AUG2020bhav.csv')   
df = pd.DataFrame(data, columns= ['SYMBOL','SERIES','OPEN','HIGH','LOW','CLOSE','LAST','PREVCLOSE','TOTTRDQTY','TOTTRDVAL','TIMESTAMP','TOTALTRADES','ISIN'])

# conn = pyodbc.connect('DRIVER={MySQL ODBC 4.0.30 Driver};User ID=root;Password=;Server=localhost;Database=nse_data;Port=3306;String Types=Unicode')

conn =mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

cursor = conn.cursor()

for row in df.itertuples():
    cursor.execute('''''''''''''
                INSERT INTO nse_data.dbo.historical_daily_data (SYMBOL, SERIES, OPEN, HIGH, LOW, CLOSE, LAST, PREVCLOSE, TOTTRDQTY, TOTTRDVAL, TIMESTAMP, TOTALTRADES, ISIN)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
                ''''''''''''',
                row.SYMBOL, 
                row.SERIES,
                row.OPEN,
                row.HIGH,
                row.LOW,
                row.CLOSE,
                row.LAST,
                row.PREVCLOSE,
                row.TOTTRDQTY,
                row.TOTTRDVAL,
                row.TIMESTAMP,
                row.TOTALTRADES,
                row.ISIN,
                )
conn.commit()