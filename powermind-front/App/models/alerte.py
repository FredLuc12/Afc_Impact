# app/models/alerte.py

from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any

from app.models.base import (
    AlerteCriticite,
    AlerteStatut,
    AppBaseModel,
    UUIDTimestampedModel,
)

class AlerteBase(AppBaseModel):
    # On garde capteur_id comme lien principal
    capteur_id: UUID
    # Changement de 'type' en 'titre' pour matcher ton UI
    titre: str 
    # Changement de 'criticite' en 'niveau' (ex: critical, warning, info)
    niveau: str 
    message: Optional[str] = None
    statut: AlerteStatut = 'active'
    # Champ pour accueillir les infos du capteur lors d'une jointure (nom, etc.)
    capteurs: Optional[Dict[str, Any]] = None 

class Alerte(AlerteBase, UUIDTimestampedModel):
    """Modèle complet représentant une alerte en base de données."""
    pass

class AlerteCreate(AppBaseModel):
    """Modèle pour la création d'une nouvelle alerte."""
    capteur_id: UUID
    titre: str
    niveau: str
    message: Optional[str] = None
    statut: AlerteStatut = 'active'

class AlerteUpdate(AppBaseModel):
    """Modèle pour la mise à jour d'une alerte existante."""
    titre: Optional[str] = None
    niveau: Optional[str] = None
    message: Optional[str] = None
    statut: Optional[AlerteStatut] = None

class AlerteSummary(AppBaseModel):
    """Modèle simplifié pour les listes ou les résumés."""
    id: UUID
    capteur_id: UUID
    titre: str
    niveau: str
    statut: AlerteStatut
    created_at: datetime
    capteurs: Optional[Dict[str, Any]] = None