from contextlib import contextmanager
import os, time
from psycopg2 import pool
from psycopg2.extras import RealDictCursor

class Sql:
    def __init__(
        self,
        dbname=None,
        user=None,
        password=None,
        host=None,
        port=None,
        min_connections=1,
        max_connections=5,
        namespace: str = "public",
        retries: int = 5,
        retry_delay: float = 2.0
    ):
        self.dbname = dbname or os.environ.get("DB_NAME")
        self.user = user or os.environ.get("DB_USER")
        self.password = password or os.environ.get("DB_PASSWORD")
        self.host = host or os.environ.get("DB_HOST")
        self.port = port or int(os.environ.get("DB_PORT", 5432))

        if not all([self.dbname, self.user, self.password, self.host]):
            raise ValueError("Missing DB connection configuration")

        self.namespace = namespace

        self.pool = self._create_pool(
            min_connections,
            max_connections,
            retries,
            retry_delay
        )

        self._enums = {}
        self._enums_loaded = False

    @property
    def enums(self):
        if not self._enums_loaded:
            self._enums = self._get_enums()
            self._enums_loaded = True
        return self._enums
    def _create_pool(self, min_c, max_c, retries, delay):
        last_exc = None
        for attempt in range(1, retries + 1):
            try:
                return pool.ThreadedConnectionPool(
                    min_c,
                    max_c,
                    dbname=self.dbname,
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port
                )
            except Exception as e:
                last_exc = e
                if attempt < retries:
                    time.sleep(delay)
                    continue
                raise RuntimeError(f"Postgres connection error: {e}") from e

    def close(self):
        if self.pool:
            self.pool.closeall()
    @contextmanager
    def connection(self):
        conn = self.pool.getconn()
        try:
            yield conn
        finally:
            self.pool.putconn(conn)

    @contextmanager
    def transaction(self):
        with self.connection() as conn:
            try:
                yield conn
                conn.commit()
            except Exception:
                conn.rollback()
                raise
    @staticmethod
    def _is_write_statement(sql):
        statement = sql.lstrip().split(None, 1)[0].upper()
        return statement in {"INSERT", "UPDATE", "DELETE", "CREATE", "ALTER", "DROP", "TRUNCATE", "COPY"}

    def execute(self, sql, params=None, fetchone=False, fetchall=False, commit=False):
        print(f"""
Sql: {sql}, params: {params}, fetchone: {fetchone}, fetchall: {fetchall}, commit: {commit}
        """)
        params = params or ()

        with self.connection() as conn:
            try:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    print("llegó aquí, nivel 1")
                    cur.execute(sql, params)

                    if self._is_write_statement(sql) or commit:
                        print("Llegó aquí, nivel 2")
                        conn.commit()

                    if fetchone:
                        return cur.fetchone()
                    if fetchall:
                        return cur.fetchall()
            except Exception as e:
                print("No llegó", e)
                conn.rollback()
                raise

    def query(self, sql, params=None):
        with self.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params, self)
            conn.commit()

    def fetchone(self, sql, params=None):
        return self.execute(sql, params, fetchone=True)

    def fetchall(self, sql, params=None):
        return self.execute(sql, params, fetchall=True)

    def scalar(self, sql, params=None):
        row = self.fetchone(sql, params)
        if not row:
            return None
        return next(iter(row.values()))

    def exists(self, sql, params=None):
        return self.scalar(sql, params) is not None
    def _get_enums(self) -> dict:
        rows = self.fetchall("""
            SELECT
                t.typname AS enum_name,
                array_agg(e.enumlabel ORDER BY e.enumsortorder) AS values
            FROM pg_type t
            JOIN pg_enum e ON e.enumtypid = t.oid
            JOIN pg_namespace n ON n.oid = t.typnamespace
            WHERE n.nspname = %s
            GROUP BY t.typname
        """, (self.namespace,))

        return {row["enum_name"]: row["values"] for row in rows}
    def create_table(self, tablename: str, columns: dict | None = None, if_not_exists: bool = True, replace: bool = False):
        default_columns = {
            "id": "BIGSERIAL PRIMARY KEY",
            "created_at": "TIMESTAMP NOT NULL DEFAULT NOW()",
            "updated_at": "TIMESTAMP NOT NULL DEFAULT NOW()",
            "deleted_at": "TIMESTAMP"
        }

        if columns is None:
            columns = default_columns if if_not_exists or replace else None

        if not columns:
            raise ValueError("Columns must be provided when if_not_exists=False")

        col_sql = ", ".join(
            f"{name} {definition}"
            for name, definition in columns.items()
        )

        with self.transaction() as conn:
            with conn.cursor() as cur:
                if replace:
                    cur.execute(f"DROP TABLE IF EXISTS {tablename}")

                sql = (
                    f"CREATE TABLE {'IF NOT EXISTS ' if if_not_exists and not replace else ''}"
                    f"{tablename} ({col_sql})"
                )
                cur.execute(sql)

    def drop_table(self, tablename: str, if_exists: bool = True):
        sql = (
            f"DROP TABLE {'IF EXISTS ' if if_exists else ''}"
            f"{tablename}"
        )

        with self.transaction() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                