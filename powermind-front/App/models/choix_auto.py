# app/models/choix_auto.py
# STRUCTURE BDD RÉELLE:
# choix_auto: id (int8 PK), choix (text) — ATTENTION: colonne 'choix' pas 'mode'/'energie_choisie'
# Pas de FK installation_id dans cette table

from app.models.base import AppBaseModel


class ChoixAutoBase(AppBaseModel):
    choix: str  # ATTENTION: colonne 'choix' en BDD (ex: 'electric', 'gaz')


class ChoixAuto(ChoixAutoBase):
    id: int  # int8 en BDD


class ChoixAutoCreate(ChoixAutoBase):
    pass


class ChoixAutoUpdate(AppBaseModel):
    choix: str | None = None
