import csv
import MySQLdb
import pymysql

db = pymysql.connect(
        host="localhost",
        port=3308,
        user="root",
        passwd="",
        db="nse_data"
 )
cursor = db.cursor()

csv_data = csv.reader(r'E:\py_docs\cm03AUG2020bhav.csv')
next(csv_data)
for row in csv_data:

    cursor.execute('INSERT INTO historical_daily_data(SYMBOL, SERIES, OPEN, HIGH, LOW, CLOSE, LAST, PREVCLOSE, TOTTRDQTY, TOTTRDVAL, TIMESTAMP, TOTALTRADES, ISIN ) VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")', row)
db.commit()
cursor.close()
print("Done")