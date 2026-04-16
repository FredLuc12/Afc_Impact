# app/models/alerte.py
# STRUCTURE BDD RÉELLE:
# alertes: capteur_id (uuid FK), message (text)
# Pas de 'titre', pas de 'niveau', pas d'id propre défini, pas de 'statut' en BDD

from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any

from app.models.base import AppBaseModel, UUIDTimestampedModel


class AlerteBase(AppBaseModel):
    capteur_id: UUID
    message: str  # Seuls champs réels de la table alertes


class Alerte(AlerteBase, UUIDTimestampedModel):
    """Modèle complet représentant une alerte en base de données."""
    # Champ de jointure optionnel (capteurs.nom via jointure)
    capteurs: Optional[Dict[str, Any]] = None


class AlerteCreate(AppBaseModel):
    """Modèle pour la création d'une nouvelle alerte."""
    capteur_id: UUID
    message: str


class AlerteUpdate(AppBaseModel):
    """Modèle pour la mise à jour d'une alerte existante."""
    message: Optional[str] = None


class AlerteSummary(AppBaseModel):
    """Modèle simplifié pour les listes."""
    id: UUID
    capteur_id: UUID
    message: str
    created_at: datetime
    capteurs: Optional[Dict[str, Any]] = None
