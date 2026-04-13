#  Système de Supervision IoT (TP1)

Ce projet réalise la supervision automatisée d'un bâtiment connecté. Il centralise les données de capteurs environnementaux (température, humidité, mouvement) installés dans différentes salles pour les afficher sur un tableau de bord web et déclencher des alertes e-mail en cas de dépassement de seuil.

##  Architecture du Système

Le système repose sur une architecture **Hub-and-Spoke** (en étoile).



### Composantes
* **Nœuds Capteurs (Parcours A - ESP8266) :** Acquièrent les données et les envoient par HTTP POST (JSON)
* **Superviseur Central (Parcours B - Arduino Uno R4 WiFi) :** Centralise les données, héberge l'API JSON et gère les seuils d'alerte
* **Interface de Supervision (Front-end NiceGUI) :** Tableau de bord web pour la visualisation des données en temps réel
* **Système de Notification (Make.com) :** Service cloud déclenchant des e-mails d'alerte



##  Nœuds Capteurs (Parcours A - ESP8266)

Chaque nœud est basé sur un ESP8266 NodeMCU connecté au WiFi "Ansumdine".

* **Matériel :** DHT11 (Temp/Hum) sur D4/GPIO2, PIR sur D5/GPIO14
* **Fonctionnement :** Envoi des données toutes les 5 secondes au superviseur
* **Format de donnée :** JSON

```json
{
  "room": "salle1",
  "temperature": 21.3,
  "humidity": 59.0,
  "pir": 1,
  "timestamp": 450938
}
```
##  Superviseur Central (Parcours B - Arduino)

L'Arduino **Uno R4 WiFi** agit comme le **cerveau du système** (`IP: 10.130.13.100`).

### API JSON

**POST** : Réception des données des ESP8266 et mise à jour des variables globales.  
**GET** : Exposition des données agrégées au front-end **NiceGUI** avec headers **CORS** activés.

###  Système d’Alerte (Make.com)

Si la **température dépasse 28.0°C**, une requête **GET** est envoyée au **webhook Make.com** pour déclencher un e-mail.

---

##  Interface Web (Front-end NiceGUI)

L’interface utilisateur est développée en **Python** avec le framework **NiceGUI**.

**Réactivité** : L’affichage est mis à jour en temps réel côté serveur et poussé vers le navigateur sans JavaScript manuel côté client.  
**Stockage** : Les données sont traitées et stockées dans une base de données **SQLite**.



##  Guide d’Installation Rapide

**Matériel** : Connecter les **ESP8266** et l’**Arduino** au WiFi `"Ansumdine"`.  
**Configuration** : Vérifier que le superviseur est configuré sur l’IP `10.130.13.100`.  
**Lancement** : Lancer l’application **NiceGUI** pour afficher le front-end dans un navigateur.  
**Test** : Chauffer un **capteur DHT11** au-dessus de **28°C** pour vérifier le déclenchement de l’alerte.
