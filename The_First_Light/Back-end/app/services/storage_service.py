"""
Service de stockage des images uploadées
Organisation: /uploads/{user_id}/{timestamp}_{filename}
"""

import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional
import shutil


class StorageService:
    """Service pour gérer le stockage des images sur le serveur"""

    def __init__(self, base_upload_dir: str = "uploads"):
        """
        Initialise le service de stockage

        Args:
            base_upload_dir: Répertoire de base pour les uploads
        """
        self.base_upload_dir = Path(base_upload_dir)
        self._ensure_base_directory()

    def _ensure_base_directory(self):
        """Crée le répertoire de base s'il n'existe pas"""
        self.base_upload_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 Répertoire d'upload: {self.base_upload_dir.absolute()}")

    def _get_user_directory(self, user_id: str) -> Path:
        """
        Retourne le répertoire pour un utilisateur spécifique

        Args:
            user_id: ID de l'utilisateur

        Returns:
            Path: Chemin vers le répertoire utilisateur
        """
        user_dir = self.base_upload_dir / user_id
        user_dir.mkdir(parents=True, exist_ok=True)
        return user_dir

    def _generate_unique_filename(self, original_filename: str) -> str:
        """
        Génère un nom de fichier unique

        Args:
            original_filename: Nom original du fichier

        Returns:
            str: Nom de fichier unique
        """
        # Extraire l'extension
        file_ext = os.path.splitext(original_filename)[1].lower()

        # Créer un nom unique: timestamp_uuid.ext
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]

        return f"{timestamp}_{unique_id}{file_ext}"

    def save_image(
        self,
        user_id: str,
        filename: str,
        file_content: bytes
    ) -> str:
        """
        Sauvegarde une image sur le serveur

        Args:
            user_id: ID de l'utilisateur
            filename: Nom original du fichier
            file_content: Contenu binaire du fichier

        Returns:
            str: Chemin relatif du fichier sauvegardé
        """
        # Obtenir le répertoire utilisateur
        user_dir = self._get_user_directory(user_id)

        # Générer un nom de fichier unique
        unique_filename = self._generate_unique_filename(filename)

        # Chemin complet du fichier
        file_path = user_dir / unique_filename

        # Sauvegarder le fichier
        with open(file_path, 'wb') as f:
            f.write(file_content)

        # Retourner le chemin relatif
        relative_path = f"{user_id}/{unique_filename}"
        print(f"💾 Image sauvegardée: {relative_path}")

        return relative_path

    def get_image_path(self, relative_path: str) -> Optional[Path]:
        """
        Récupère le chemin complet d'une image

        Args:
            relative_path: Chemin relatif de l'image (user_id/filename)

        Returns:
            Path: Chemin complet du fichier ou None si n'existe pas
        """
        full_path = self.base_upload_dir / relative_path

        if full_path.exists() and full_path.is_file():
            return full_path

        return None

    def delete_image(self, relative_path: str) -> bool:
        """
        Supprime une image

        Args:
            relative_path: Chemin relatif de l'image

        Returns:
            bool: True si suppression réussie, False sinon
        """
        full_path = self.base_upload_dir / relative_path

        try:
            if full_path.exists() and full_path.is_file():
                full_path.unlink()
                print(f"🗑️  Image supprimée: {relative_path}")
                return True
            return False
        except Exception as e:
            print(f"❌ Erreur suppression image: {e}")
            return False

    def delete_user_images(self, user_id: str) -> bool:
        """
        Supprime toutes les images d'un utilisateur

        Args:
            user_id: ID de l'utilisateur

        Returns:
            bool: True si suppression réussie, False sinon
        """
        user_dir = self.base_upload_dir / user_id

        try:
            if user_dir.exists() and user_dir.is_dir():
                shutil.rmtree(user_dir)
                print(f"🗑️  Dossier utilisateur supprimé: {user_id}")
                return True
            return False
        except Exception as e:
            print(f"❌ Erreur suppression dossier: {e}")
            return False

    def get_user_images_count(self, user_id: str) -> int:
        """
        Compte le nombre d'images d'un utilisateur

        Args:
            user_id: ID de l'utilisateur

        Returns:
            int: Nombre d'images
        """
        user_dir = self.base_upload_dir / user_id

        if not user_dir.exists():
            return 0

        return len(list(user_dir.glob("*")))

    def get_storage_stats(self) -> dict:
        """
        Retourne des statistiques sur le stockage

        Returns:
            dict: Statistiques (nombre de users, nombre total d'images, taille)
        """
        users = [d for d in self.base_upload_dir.iterdir() if d.is_dir()]
        total_images = sum(len(list(user_dir.glob("*"))) for user_dir in users)

        # Calculer la taille totale
        total_size = sum(
            f.stat().st_size
            for user_dir in users
            for f in user_dir.glob("*")
            if f.is_file()
        )

        return {
            "users_count": len(users),
            "total_images": total_images,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2)
        }


# Instance singleton
_storage_service: Optional[StorageService] = None


def get_storage_service() -> StorageService:
    """
    Retourne l'instance singleton du service de stockage

    Returns:
        StorageService: Instance du service
    """
    global _storage_service

    if _storage_service is None:
        _storage_service = StorageService()

    return _storage_service
