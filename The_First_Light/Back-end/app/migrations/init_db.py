from DBHandler import DBHandler
from User import User
from Analyse import Analyse

#  Créer le gestionnaire de base de données
db = DBHandler(
    dbname="mothra_db",
    user="postgres",
    password="root",
    host="localhost",
    port="5432"
)

#  Se connecter
db.connect()

#  Créer les tables
db.create_tables()

#  Lier la BDD aux classes
User.db = db
Analyse.db = db 

#  Déconnecter proprement
db.disconnect()