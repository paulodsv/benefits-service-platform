import time
import psycopg2
from psycopg2 import pool
from psycopg2 import OperationalError
from app.config import DATABASE_URL

_pool = None

def init_db_pool(minconn=1, maxconn=5, retries=30, delay=1):
    """Inicializa o pool de conexões com o banco de dados Postgres.
    retries: number of attempts (default 30)
    delay: seconds between attempts (default 1)
    """
    global _pool
    if _pool is None:
        last_exc = None
        for attempt in range(1, retries + 1):
            try:
                _pool = psycopg2.pool.SimpleConnectionPool(minconn, maxconn, DATABASE_URL)
                return _pool
            except OperationalError as e:
                last_exc = e
                print(f"init_db_pool: Postgres not ready (attempt {attempt}/{retries}), retrying in {delay}s...")
                time.sleep(delay)
        # Se chegar aqui, todas as tentativas falharam
        print("init_db_pool: Could not connect to Postgres after retries; raising last exception")
        raise last_exc
    return _pool

def get_conn():
    global _pool
    if _pool is None:
        init_db_pool()
    return _pool.getconn()

def put_conn(conn):
    global _pool
    if _pool:
        _pool.putconn(conn)

def query(sql, params=None, fetchone=False, fetchall=False, commit=False):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(sql, params or ())
        if commit:
            conn.commit()
        if fetchone:
            return cur.fetchone()
        if fetchall:
            return cur.fetchall()
        return None
    finally:
        try:
            cur.close()
        except:
            pass
        put_conn(conn)
