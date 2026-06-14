import sys, os
sys.path.insert(0, '/www/wwwroot/202606AICRM/backend')
os.chdir('/www/wwwroot/202606AICRM')
os.environ['APP_ENV'] = 'development'

from app.core.database import init_db, SessionLocal
from sqlalchemy import text

init_db()
db = SessionLocal()

try:
    # Check admin
    r = db.execute(text("SELECT id FROM users WHERE username='admin'")).fetchone()
    if r:
        print('Admin exists, ID:', r[0])
    else:
        db.execute(text(
            "INSERT INTO users (username, password_hash, display_name, email, role, is_active, created_at, updated_at) "
            "VALUES ('admin', 'temp', 'Admin', 'a@h.com', 'admin', 1, datetime('now'), datetime('now'))"
        ))
        db.commit()
        print('Admin created')

    # List tables
    r = db.execute(text("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")).fetchall()
    print('Tables:', [x[0] for x in r])

    # Count users
    r = db.execute(text('SELECT COUNT(*) FROM users')).fetchone()
    print('User count:', r[0])

finally:
    db.close()
