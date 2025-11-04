import datetime
import uuid

class Analyse():

    db = None

    def __init__(self, user_id, photo, diagnostic, confidence):

        self.user_id = self.valide_owner(user_id)
        self.photo = self.valide_photo(photo)
        self.diagnostic = self.valide_diagnostic(diagnostic)
        self.confidence = self.valide_confidence(confidence)

        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now()

    def save(self):
        if not Analyse.db:
            raise ConnectionError("DBHandler non défini pour User")
        
        query="""
            INSERT INTO analyses (id, user_id, photo, diagnostic, confidence, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """

        params = (
            self.id,
            self.user_id,
            self.photo,
            self.diagnostic,
            self.confidence,
            self.created_at
        )
        Analyse.db.execute(query, params)

    @classmethod
    def get_by_id(cls, analyse_id):
        """Récupère une analyse par son ID"""
        if not cls.db:
            raise ConnectionError("DBHandler non défini pour Analyse")

        query = "SELECT * FROM analyses WHERE id = %s"
        result = cls.db.fetch_one(query, (analyse_id,))

        if not result:
            return None

        return cls._from_db(result)

    @classmethod
    def get_by_user(cls, user_id):
        """Récupère toutes les analyses d'un utilisateur"""
        if not cls.db:
            raise ConnectionError("DBHandler non défini pour Analyse")

        query = "SELECT * FROM analyses WHERE user_id = %s ORDER BY created_at DESC"
        results = cls.db.fetch_all(query, (user_id,))

        return [cls._from_db(row) for row in results]

    @classmethod
    def _from_db(cls, row):
        """Crée une instance Analyse depuis une ligne de BD"""
        analyse = cls.__new__(cls)
        analyse.id = row['id']
        analyse.user_id = row['user_id']
        analyse.photo = row['photo']
        analyse.diagnostic = row['diagnostic']
        analyse.confidence = float(row['confidence'])
        analyse.created_at = row['created_at']
        return analyse

    def valide_owner(self, user_id):
        """Vérifie que l'user_id est bien un UUID valide et correspond à un utilisateur existant"""
        if not isinstance(user_id, str):
            raise ValueError("user_id doit être une chaîne")
        try:
            uuid.UUID(user_id)
        except ValueError:
            raise ValueError("user_id invalide (UUID attendu)")
        return user_id

    def valide_photo(self, photo):
        """Vérifie que la photo est bien liée à l'analyse (format, nom, etc.)"""
        if not isinstance(photo, str) or not photo.strip():
            raise ValueError("photo invalide")
        if not photo.lower().endswith(('.jpg', 'jpeg', 'png', 'webp')):
            raise ValueError("format non supporté")
        return photo

    def valide_diagnostic(self, diagnostic):
        """Vérifie que le diagnostic est cohérent et bien formaté"""
        if not isinstance(diagnostic, str) or not diagnostic.strip():
            raise ValueError("diagnostic invalide")
        if len(diagnostic) > 2000:
            raise ValueError("diagnostic trop long")
        return diagnostic

    def valide_confidence(self, confidence):
        """Vérifie que le taux de confiance est un nombre valide"""
        try: c = float(confidence)
        except Exception:
            raise ValueError("confidence doit être numérique")
        if not (0.0 <= c <= 1):
            raise ValueError("confidence hors plage")
        return c

    def delete(self):
        """Supprime l'analyse de la base de données"""
        if not Analyse.db:
            raise ConnectionError("DBHandler non défini pour Analyse")

        query = "DELETE FROM analyses WHERE id = %s"
        Analyse.db.execute(query, (self.id,))

    def to_dict(self):
        """Convertit l'analyse en dictionnaire (pour JSON)"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "photo": self.photo,
            "diagnostic": self.diagnostic,
            "confidence": self.confidence,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime.datetime) else self.created_at
        }