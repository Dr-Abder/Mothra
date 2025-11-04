import datetime
import uuid
import re
import bcrypt

class User():

    used_emails = set()
    db = None

    def __init__(self, first_name, last_name, email, password, age, sex):

        self.first_name = self.valide_name(first_name)
        self.last_name = self.valide_name(last_name)
        self.email = self.valide_email(email)
        self.valide_password(password)
        self.password_hash = self.hash_password(password)
        self.age = self.valide_age(age)
        self.sex = self.valide_sex(sex)

        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.analyses = []

    def save(self):
        if not User.db:
            raise ConnectionError("DBHandler non défini pour User")

        query = """
            INSERT INTO users (id, first_name, last_name, email, password_hash, age, sex, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """
        params = (
            self.id,
            self.first_name,
            self.last_name,
            self.email,
            self.password_hash.decode(),  # bcrypt hash est en bytes
            self.age,
            self.sex,
            self.created_at,
            self.updated_at
        )
        User.db.execute(query, params)

    @classmethod
    def get_by_id(cls, user_id):
        """Récupère un utilisateur par son ID"""
        if not cls.db:
            raise ConnectionError("DBHandler non défini pour User")

        query = "SELECT * FROM users WHERE id = %s"
        result = cls.db.fetch_one(query, (user_id,))

        if not result:
            return None

        return cls._from_db(result)

    @classmethod
    def get_by_email(cls, email):
        """Récupère un utilisateur par son email"""
        if not cls.db:
            raise ConnectionError("DBHandler non défini pour User")

        query = "SELECT * FROM users WHERE email = %s"
        result = cls.db.fetch_one(query, (email.lower(),))

        if not result:
            return None

        return cls._from_db(result)

    @classmethod
    def _from_db(cls, row):
        """Crée une instance User depuis une ligne de BD"""
        user = cls.__new__(cls)
        user.id = row['id']
        user.first_name = row['first_name']
        user.last_name = row['last_name']
        user.email = row['email']
        user.password_hash = row['password_hash'].encode() if isinstance(row['password_hash'], str) else row['password_hash']
        user.age = row['age']
        user.sex = row['sex']
        user.created_at = row['created_at']
        user.updated_at = row['updated_at']
        user.analyses = []
        return user

    def valide_name(self, name):
        name = name.strip()
        name = name.capitalize()
        if len(name) > 50:
            raise  ValueError("Nom invalide")
        elif not name.isalpha():
            raise  ValueError("Nom invalide")
        return name

    def valide_email(self, email):
        email = email.lower()
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            raise ValueError("Email invalide")
        # Note: La vérification de l'unicité se fait via la contrainte UNIQUE de la base
        return email

    def valide_password(self, password):
        if not re.match(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", password):
            raise ValueError("Mot de passe invalide")
        return password

    def hash_password(self, password):
        bytes = password.encode()
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(bytes, salt)

    def verify_password(self, password):
        bytes = password.encode()
        return bcrypt.checkpw(bytes, self.password_hash)

    def valide_age(self, age):
        if not isinstance(age, int) or age <= 0:
            raise ValueError("Âge invalide")
        return age

    def valide_sex(self, sex):
        mf_sex = ["homme", "femme"]
        if sex.lower() not in mf_sex:
            raise ValueError("Sexe invalide")
        return sex

    def update(self):
        """Met à jour l'utilisateur dans la base de données"""
        if not User.db:
            raise ConnectionError("DBHandler non défini pour User")

        self.updated_at = datetime.datetime.now()

        query = """
            UPDATE users
            SET first_name = %s, last_name = %s, email = %s,
                password_hash = %s, age = %s, sex = %s, updated_at = %s
            WHERE id = %s
        """
        params = (
            self.first_name,
            self.last_name,
            self.email,
            self.password_hash.decode() if isinstance(self.password_hash, bytes) else self.password_hash,
            self.age,
            self.sex,
            self.updated_at,
            self.id
        )
        User.db.execute(query, params)

    def delete(self):
        """Supprime l'utilisateur de la base de données"""
        if not User.db:
            raise ConnectionError("DBHandler non défini pour User")

        query = "DELETE FROM users WHERE id = %s"
        User.db.execute(query, (self.id,))

    def to_dict(self):
        """Convertit l'utilisateur en dictionnaire (pour JSON)"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "age": self.age,
            "sex": self.sex,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime.datetime) else self.created_at,
            "updated_at": self.updated_at.isoformat() if isinstance(self.updated_at, datetime.datetime) else self.updated_at,
            "analyses": [analyse.to_dict() if hasattr(analyse, 'to_dict') else analyse for analyse in self.analyses]
        }