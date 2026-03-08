import sqlite3
import os

# Migration script ensures required columns exist in tasks table

db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'career_ai.db'))
print('DB path', db_path)
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("PRAGMA table_info(tasks);")
cols = [r[1] for r in cur.fetchall()]
print('Existing columns:', cols)

if 'score' not in cols:
    print('Adding score column')
    cur.execute('ALTER TABLE tasks ADD COLUMN score FLOAT DEFAULT 0.0')
    conn.commit()
    print('Score column added')
else:
    print('Score column already exists')

if 'completed_at' not in cols:
    print('Adding completed_at column')
    cur.execute('ALTER TABLE tasks ADD COLUMN completed_at DATETIME NULL')
    conn.commit()
    print('completed_at column added')
else:
    print('completed_at column already exists')

if 'created_at' not in cols:
    print('Adding created_at column')
    # SQLite cannot add a column with a non-constant default via ALTER TABLE
    cur.execute('ALTER TABLE tasks ADD COLUMN created_at DATETIME NULL')
    conn.commit()
    print('created_at column added (nullable)')
else:
    print('created_at column already exists')

conn.close()
