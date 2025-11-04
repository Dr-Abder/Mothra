import psycopg2

class DBHandler():

    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port


    def connect(self):
        try:
            self.conn = psycopg2.connect(
                    dbname=self.dbname,
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port
                    )
            self.cur = self.conn.cursor()
        except psycopg2.OperationalError as e:
            raise ConnectionError(f"Connexion impossible : {e}")

    def disconnect(self):
        self.cur.close()
        self.conn.close()

    def execute(self, query, params=None):
        if params:
            self.cur.execute(query, params)
        else:
            self.cur.execute(query)
        if query.strip().upper().startswith("SELECT"):
            return self.cur.fetchall()
        self.conn.commit()

    def fetch_one(self, query, params=None):
        """Exécute une requête et retourne un seul résultat sous forme de dictionnaire"""
        if params:
            self.cur.execute(query, params)
        else:
            self.cur.execute(query)

        row = self.cur.fetchone()
        if row is None:
            return None

        # Convertir le tuple en dictionnaire
        columns = [desc[0] for desc in self.cur.description]
        return dict(zip(columns, row))

    def fetch_all(self, query, params=None):
        """Exécute une requête et retourne tous les résultats sous forme de liste de dictionnaires"""
        if params:
            self.cur.execute(query, params)
        else:
            self.cur.execute(query)

        rows = self.cur.fetchall()
        if not rows:
            return []

        # Convertir chaque tuple en dictionnaire
        columns = [desc[0] for desc in self.cur.description]
        return [dict(zip(columns, row)) for row in rows]

    def create_tables(self):
        sql_users = """CREATE TABLE IF NOT EXISTS users(
                        id UUID PRIMARY KEY,
                        first_name VARCHAR(50) NOT NULL,
                        last_name VARCHAR(50) NOT NULL,
                        email VARCHAR(255) NOT NULL UNIQUE,
                        password_hash TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        sex VARCHAR (10) NOT NULL,
                        skin_type VARCHAR(30),
                        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                        updated_at TIMESTAMP NOT NULL DEFAULT NOW()
                    );"""
        sql_analyses = """CREATE TABLE IF NOT EXISTS analyses(
                        id UUID PRIMARY KEY,
                        user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                        photo TEXT NOT NULL,
                        diagnostic TEXT NOT NULL,
                        confidence REAL NOT NULL,
                        created_at TIMESTAMP NOT NULL DEFAULT NOW()
                    );"""

        self.execute(sql_users)
        self.execute(sql_analyses)