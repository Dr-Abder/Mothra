"""
Fichier de test pour les classes User et Analyse
Teste toutes les méthodes CRUD
"""

from DBHandler import DBHandler
from User import User
from Analyse import Analyse

def test_user_crud():
    """Test complet du CRUD pour User"""
    print("\n" + "="*50)
    print("TEST USER - CRUD COMPLET")
    print("="*50)

    # CREATE - Créer un utilisateur
    print("\n[1] CREATE - Création d'un utilisateur...")
    try:
        user = User("Jean", "Dupont", "jean.dupont@example.com", "Pass@1234", 25, "homme")
        user.save()
        print(f"Utilisateur créé avec ID: {user.id}")
        user_id = user.id
    except Exception as e:
        print(f"Erreur lors de la création: {e}")
        return

    # READ - Récupérer par ID
    print("\n[2] READ - Récupération par ID...")
    try:
        retrieved_user = User.get_by_id(user_id)
        if retrieved_user:
            print(f" Utilisateur récupéré: {retrieved_user.first_name} {retrieved_user.last_name}")
            print(f"   Email: {retrieved_user.email}")
            print(f"   Âge: {retrieved_user.age}")
        else:
            print(" Utilisateur non trouvé")
    except Exception as e:
        print(f" Erreur lors de la récupération: {e}")

    # READ - Récupérer par email
    print("\n[3] READ - Récupération par email...")
    try:
        user_by_email = User.get_by_email("jean.dupont@example.com")
        if user_by_email:
            print(f" Utilisateur trouvé par email: {user_by_email.first_name}")
        else:
            print(" Utilisateur non trouvé par email")
    except Exception as e:
        print(f" Erreur lors de la récupération par email: {e}")

    # VERIFY PASSWORD - Vérifier le mot de passe
    print("\n[4] AUTH - Vérification du mot de passe...")
    try:
        is_valid = retrieved_user.verify_password("Pass@1234")
        if is_valid:
            print(" Mot de passe correct")
        else:
            print(" Mot de passe incorrect")
    except Exception as e:
        print(f" Erreur lors de la vérification: {e}")

    # UPDATE - Mettre à jour l'utilisateur
    print("\n[5] UPDATE - Mise à jour de l'utilisateur...")
    try:
        retrieved_user.age = 26
        retrieved_user.first_name = "Jean-Pierre"
        retrieved_user.update()
        print(" Utilisateur mis à jour")

        # Vérifier la mise à jour
        updated_user = User.get_by_id(user_id)
        print(f"   Nouveau prénom: {updated_user.first_name}")
        print(f"   Nouvel âge: {updated_user.age}")
    except Exception as e:
        print(f" Erreur lors de la mise à jour: {e}")

    # TO_DICT - Conversion en JSON
    print("\n[6] TO_DICT - Conversion en dictionnaire...")
    try:
        user_dict = updated_user.to_dict()
        print(" Conversion réussie:")
        print(f"   {user_dict}")
    except Exception as e:
        print(f" Erreur lors de la conversion: {e}")

    # DELETE - Supprimer l'utilisateur
    print("\n[7] DELETE - Suppression de l'utilisateur...")
    try:
        updated_user.delete()
        print(" Utilisateur supprimé")

        # Vérifier la suppression
        deleted_user = User.get_by_id(user_id)
        if deleted_user is None:
            print(" Vérification: l'utilisateur n'existe plus")
        else:
            print(" L'utilisateur existe encore")
    except Exception as e:
        print(f" Erreur lors de la suppression: {e}")


def test_analyse_crud():
    """Test complet du CRUD pour Analyse"""
    print("\n" + "="*50)
    print("TEST ANALYSE - CRUD COMPLET")
    print("="*50)

    # Créer d'abord un utilisateur pour les tests
    print("\n[0] Préparation - Création d'un utilisateur...")
    try:
        user = User("Marie", "Martin", "marie.martin@example.com", "SecurePass@123", 30, "femme")
        user.save()
        print(f" Utilisateur créé avec ID: {user.id}")
        user_id = user.id
    except Exception as e:
        print(f" Erreur lors de la création de l'utilisateur: {e}")
        return

    # CREATE - Créer une analyse
    print("\n[1] CREATE - Création d'une analyse...")
    try:
        analyse = Analyse(
            user_id=user_id,
            photo="scan_peau_001.jpg",
            diagnostic="Mélanome détecté - Consultation urgente recommandée",
            confidence=0.92
        )
        analyse.save()
        print(f" Analyse créée avec ID: {analyse.id}")
        analyse_id = analyse.id
    except Exception as e:
        print(f" Erreur lors de la création: {e}")
        return

    # CREATE - Créer une deuxième analyse
    print("\n[2] CREATE - Création d'une seconde analyse...")
    try:
        analyse2 = Analyse(
            user_id=user_id,
            photo="scan_peau_002.png",
            diagnostic="Aucune anomalie détectée",
            confidence=0.98
        )
        analyse2.save()
        print(f" Seconde analyse créée avec ID: {analyse2.id}")
    except Exception as e:
        print(f" Erreur lors de la création: {e}")

    # READ - Récupérer par ID
    print("\n[3] READ - Récupération d'une analyse par ID...")
    try:
        retrieved_analyse = Analyse.get_by_id(analyse_id)
        if retrieved_analyse:
            print(f" Analyse récupérée")
            print(f"   Photo: {retrieved_analyse.photo}")
            print(f"   Diagnostic: {retrieved_analyse.diagnostic}")
            print(f"   Confiance: {retrieved_analyse.confidence}")
        else:
            print(" Analyse non trouvée")
    except Exception as e:
        print(f" Erreur lors de la récupération: {e}")

    # READ - Récupérer toutes les analyses d'un utilisateur
    print("\n[4] READ - Récupération de toutes les analyses de l'utilisateur...")
    try:
        user_analyses = Analyse.get_by_user(user_id)
        print(f" {len(user_analyses)} analyse(s) trouvée(s)")
        for i, analyse in enumerate(user_analyses, 1):
            print(f"   {i}. {analyse.photo} - Confiance: {analyse.confidence}")
    except Exception as e:
        print(f" Erreur lors de la récupération: {e}")

    # TO_DICT - Conversion en JSON
    print("\n[5] TO_DICT - Conversion en dictionnaire...")
    try:
        analyse_dict = retrieved_analyse.to_dict()
        print(" Conversion réussie:")
        print(f"   {analyse_dict}")
    except Exception as e:
        print(f" Erreur lors de la conversion: {e}")

    # DELETE - Supprimer une analyse
    print("\n[6] DELETE - Suppression de la première analyse...")
    try:
        retrieved_analyse.delete()
        print(" Analyse supprimée")

        # Vérifier la suppression
        deleted_analyse = Analyse.get_by_id(analyse_id)
        if deleted_analyse is None:
            print(" Vérification: l'analyse n'existe plus")
        else:
            print(" L'analyse existe encore")
    except Exception as e:
        print(f" Erreur lors de la suppression: {e}")

    # Vérifier qu'il reste une analyse
    print("\n[7] Vérification - Analyses restantes...")
    try:
        remaining_analyses = Analyse.get_by_user(user_id)
        print(f" {len(remaining_analyses)} analyse(s) restante(s)")
    except Exception as e:
        print(f" Erreur: {e}")

    # Nettoyage - Supprimer l'utilisateur de test
    print("\n[8] Nettoyage - Suppression de l'utilisateur de test...")
    try:
        user.delete()
        print(" Utilisateur de test supprimé")
    except Exception as e:
        print(f" Erreur lors du nettoyage: {e}")


def test_validations():
    """Test des validations"""
    print("\n" + "="*50)
    print("TEST VALIDATIONS")
    print("="*50)

    # Test validation email invalide
    print("\n[1] Test email invalide...")
    try:
        user = User("Test", "User", "email-invalide", "Pass@1234", 25, "homme")
        print(" L'email invalide a été accepté (erreur)")
    except ValueError as e:
        print(f" Email invalide rejeté: {e}")

    # Test validation mot de passe faible
    print("\n[2] Test mot de passe faible...")
    try:
        user = User("Test", "User", "test@example.com", "simple", 25, "homme")
        print(" Le mot de passe faible a été accepté (erreur)")
    except ValueError as e:
        print(f" Mot de passe faible rejeté: {e}")

    # Test validation âge négatif
    print("\n[3] Test âge invalide...")
    try:
        user = User("Test", "User", "test2@example.com", "Pass@1234", -5, "homme")
        print(" L'âge négatif a été accepté (erreur)")
    except ValueError as e:
        print(f" Âge invalide rejeté: {e}")

    # Test validation sexe invalide
    print("\n[4] Test sexe invalide...")
    try:
        user = User("Test", "User", "test3@example.com", "Pass@1234", 25, "autre")
        print(" Le sexe invalide a été accepté (erreur)")
    except ValueError as e:
        print(f" Sexe invalide rejeté: {e}")

    # Test validation photo invalide
    print("\n[5] Test format photo invalide...")
    try:
        analyse = Analyse("fake-user-id", "document.pdf", "Test", 0.5)
        print(" Le format photo invalide a été accepté (erreur)")
    except ValueError as e:
        print(f" Format photo invalide rejeté: {e}")

    # Test validation confiance hors plage
    print("\n[6] Test confiance hors plage...")
    try:
        analyse = Analyse("fake-user-id", "photo.jpg", "Test", 1.5)
        print(" La confiance hors plage a été acceptée (erreur)")
    except ValueError as e:
        print(f" Confiance hors plage rejetée: {e}")


def main():
    """Fonction principale"""
    print("\n" + "="*50)
    print("DÉBUT DES TESTS DES MODÈLES USER ET ANALYSE")
    print("="*50)

    # Connexion à la base de données
    print("\n[SETUP] Connexion à la base de données...")
    try:
        db = DBHandler(
            dbname="mothra_db",
            user="postgres",
            password="root",
            host="localhost",
            port="5432"
        )
        db.connect()
        print(" Connexion réussie")

        # Créer les tables si elles n'existent pas
        db.create_tables()
        print(" Tables créées/vérifiées")

        # Lier la base de données aux modèles
        User.db = db
        Analyse.db = db
        print(" Base de données liée aux modèles")

    except Exception as e:
        print(f" Erreur de connexion: {e}")
        return

    # Lancer les tests
    try:
        test_validations()
        test_user_crud()
        test_analyse_crud()

    except Exception as e:
        print(f"\n ERREUR GÉNÉRALE: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Déconnexion
        print("\n" + "="*50)
        print("[TEARDOWN] Déconnexion de la base de données...")
        try:
            db.disconnect()
            print(" Déconnexion réussie")
        except Exception as e:
            print(f" Erreur lors de la déconnexion: {e}")

    print("\n" + "="*50)
    print("FIN DES TESTS")
    print("="*50 + "\n")


if __name__ == "__main__":
    main()
