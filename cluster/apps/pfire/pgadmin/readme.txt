to reset account logins, run python script:


import sqlite3

db_path = '/var/lib/pgadmin/pgadmin4.db'

query = "update user set locked = false, login_attempts = 0 where username = '<admin_email>';"

conn = sqlite3.connect(db_path)

cursor = conn.cursor()

cursor.execute(query)

conn.commit()

print('User should be unlocked now. Changes commited to the DB.')