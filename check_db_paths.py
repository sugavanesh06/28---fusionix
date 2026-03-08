import os
from app.database import DATABASE_URL, engine, SessionLocal
print('DATABASE_URL from config', DATABASE_URL)
print('engine.url', engine.url)
print('cwd', os.getcwd())
from sqlalchemy import text

# try querying tables
with engine.connect() as conn:
    print('PRAGMA database_list:')
    res = conn.execute(text("PRAGMA database_list;"))
    for row in res:
        print(row)
    try:
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        print('tables in this DB:')
        for r in result:
            print(r)
    except Exception as e:
        print('error listing tables', e)

# Try connecting to other path
other_path = os.path.abspath(os.path.join(os.getcwd(), '..', 'career_ai.db'))
print('other path candidate', other_path)
from sqlalchemy import create_engine
engine2 = create_engine(f"sqlite:///{other_path}", connect_args={"check_same_thread": False})
with engine2.connect() as conn2:
    print('other engine tables:')
    try:
        result = conn2.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        for r in result:
            print(r)
    except Exception as e:
        print('error listing on engine2', e)
