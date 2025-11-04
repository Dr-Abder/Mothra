"""
Script de migration pour ajouter ON DELETE CASCADE à la contrainte de clé étrangère
"""

from DBHandler import DBHandler

def migrate():
    print("Migration: Ajout de ON DELETE CASCADE à la table analyses...")

    # Connexion à la base de données
    db = DBHandler(
        dbname="mothra_db",
        user="postgres",
        password="root",
        host="localhost",
        port="5432"
    )

    try:
        db.connect()
        print("Connexion réussie")

        # Supprimer l'ancienne contrainte
        print("\n[1] Suppression de l'ancienne contrainte de clé étrangère...")
        db.execute("ALTER TABLE analyses DROP CONSTRAINT IF EXISTS analyses_user_id_fkey;")
        print("Ancienne contrainte supprimée")

        # Ajouter la nouvelle contrainte avec ON DELETE CASCADE
        print("\n[2] Ajout de la nouvelle contrainte avec ON DELETE CASCADE...")
        db.execute("""
            ALTER TABLE analyses
            ADD CONSTRAINT analyses_user_id_fkey
            FOREIGN KEY (user_id)
            REFERENCES users(id)
            ON DELETE CASCADE;
        """)
        print("Nouvelle contrainte ajoutée")

        print("\nMigration terminée avec succès !")

    except Exception as e:
        print(f"\nErreur lors de la migration: {e}")
        import traceback
        traceback.print_exc()

    finally:
        db.disconnect()
        print("Déconnexion")

if __name__ == "__main__":
    migrate()
