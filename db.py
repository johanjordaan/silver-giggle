import mysql.connector as mysql
import config

db = mysql.connect(
    host = config.host,
    user = config.user,
    passwd = config.password
)

cursor = db.cursor()

cursor.execute('SHOW DATABASES like "%s"'%(config.database))
databases = cursor.fetchall()

if(len(databases)<1):
    print('Creating database [%s]'%(config.database))
    cursor.execute('CREATE DATABASE %s'%(config.database))
else:
    print('Database [%s] already exists'%(config.database))

cursor.execute("USE %s"%(config.database))

cursor.execute("CREATE TABLE IF NOT EXISTS event (type VARCHAR(255), dt DATETIME)")


from datetime import datetime
def add_event(type):
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    query = "INSERT INTO users (type,dt) VALUES (%s, %s)"
    values = (type, formatted_date)
    cursor.execute(query, values)
    db.commit()
