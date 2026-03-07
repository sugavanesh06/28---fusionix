import sqlite3, os
path = r"c:\Users\Hp\Downloads\cm zip\cm z\backend\career_ai.db"
print('exists', os.path.exists(path))
conn = sqlite3.connect(path)
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = c.fetchall()
print('tables', tables)
try:
    c.execute('SELECT COUNT(*) FROM resumes')
    print('resume count', c.fetchone())
except Exception as e:
    print('resume query error', e)
conn.close()
