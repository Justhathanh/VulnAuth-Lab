import pymysql

DB_CONFIG = {
    "host":     "127.0.0.1",
    "user":     "vulnuser",
    "password": "vulnpass",
    "database": "vulnauth",
    "cursorclass": pymysql.cursors.DictCursor
}

def get_db():
    return pymysql.connect(**DB_CONFIG)