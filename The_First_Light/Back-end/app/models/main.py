from DBHandler import DBHandler
from User import User
from Analyse import Analyse

# 1️⃣ Créer le gestionnaire de base de données
db = DBHandler(
    dbname="mothra_db",
    user="postgres",
    password="root",
    host="localhost",
    port="5432"
)

# 2️⃣ Se connecter
db.connect()

# 3️⃣ Créer les tables si elles n'existent pas
db.create_tables()

# 4️⃣ Lier la BDD aux classes
User.db = db
Analyse.db = db 

# 5️⃣ Exemple : créer un utilisateur
u = User("Abderrahmane", "Ghomed", "abder@example.com", "Test@1234", 20, "homme")
u.save()

# 6️⃣ Exemple : créer une analyse
a = Analyse(
    user_id=u.id,
    photo="peau1.png",
    diagnostic="Aucune anomalie détectée",
    confidence=0.98
)
a.save()

# 7️⃣ Déconnecter proprement
db.disconnect()

print("Utilisateur et analyse enregistrés avec succès !")
