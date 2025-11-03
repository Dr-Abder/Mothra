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
        if email in User.used_emails :
            raise ValueError("Cet email est déjà utilisé")
        User.used_emails.add(email)
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