import sqlite3
conn = sqlite3.connect('example.db')

c = conn.cursor()

# Do this instead
t = ('RHAT',)
c.execute('SELECT * FROM stocks WHERE symbol=?', t)
print(c.fetchall())

conn.close()

