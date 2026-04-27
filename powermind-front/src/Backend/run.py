import sqlite3
import os
import hashlib

DB_PATH = "data/suivi4k.db"

def hash_password(password):
    """Hash SHA256 sécurisé."""
    if not password:
        return ""
    return hashlib.sha256(password.encode()).hexdigest()

def get_connection():
    """Connexion à la BDD."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Crée/upgrade toutes les tables."""
    conn = get_connection()
    cursor = conn.cursor()

    # Users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # SENSOR_DATA avec MIGRATION
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL NOT NULL,
            humidite REAL NOT NULL,
            mouvement INTEGER NOT NULL,
            salle TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # MIGRATION : Ajoute colonne salle si manquante
    cursor.execute("PRAGMA table_info(sensor_data)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'salle' not in columns:
        print("Migration : Ajout colonne 'salle'")
        cursor.execute("ALTER TABLE sensor_data ADD COLUMN salle TEXT NOT NULL DEFAULT 'salle1'")
    
    # Thresholds
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS thresholds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temp_max REAL DEFAULT 28.0,
            humidite_max REAL DEFAULT 75.0,
            mouvement_actif INTEGER DEFAULT 1,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Alerts
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_data_id INTEGER,
            type_alerte TEXT,
            message TEXT,
            sent INTEGER DEFAULT 0,
            resolved INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(sensor_data_id) REFERENCES sensor_data(id)
        )
    """)

    conn.commit()
    conn.close()
    print("Tables créées/migrées")

def insert_test_data():
    """Données de test avec salle."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # User test
    password_hash = hash_password('password123')
    cursor.execute("""
        INSERT OR REPLACE INTO users (nom, prenom, email, password_hash)
        VALUES (?, ?, ?, ?)
    """, ('DUPONT', 'Jean', 'jean.dupont@email.com', password_hash))
    
    # Thresholds
    cursor.execute("INSERT OR IGNORE INTO thresholds (id, temp_max, humidite_max, mouvement_actif) VALUES (1, 28.0, 75.0, 1)")
    
    # Données test AVEC SALLE
    cursor.execute("""
        INSERT OR REPLACE INTO sensor_data (temperature, humidite, mouvement, salle)
        VALUES (24.5, 68.0, 1, 'salle1')
    """)
    cursor.execute("""
        INSERT OR REPLACE INTO sensor_data (temperature, humidite, mouvement, salle)
        VALUES (29.5, 78.0, 0, 'salle2')
    """)
    cursor.execute("""
        INSERT OR REPLACE INTO sensor_data (temperature, humidite, mouvement, salle)
        VALUES (25.0, 70.0, 1, 'salle1')
    """)
    
    # Récupère IDs pour alertes
    cursor.execute("SELECT id FROM sensor_data WHERE temperature=29.5")
    sensor_id2 = cursor.fetchone()['id']
    cursor.execute("SELECT id FROM sensor_data WHERE temperature=24.5 AND salle='salle1'")
    sensor_id1 = cursor.fetchone()['id']
    
    # 3 ALERTES TEST
    cursor.execute("""
        INSERT OR REPLACE INTO alerts (sensor_data_id, type_alerte, message, sent, resolved) 
        VALUES (?, 'temperature', 'salle2: Température dépasse 28°C : 29.5°C', 1, 0)
    """, (sensor_id2,))
    
    cursor.execute("""
        INSERT OR REPLACE INTO alerts (sensor_data_id, type_alerte, message, sent, resolved) 
        VALUES (?, 'humidite', 'salle2: Humidité dépasse 75% : 78%', 1, 1)
    """, (sensor_id2,))
    
    cursor.execute("""
        INSERT OR REPLACE INTO alerts (sensor_data_id, type_alerte, message, sent, resolved) 
        VALUES (?, 'mouvement', 'salle1: Mouvement détecté', 1, 1)
    """, (sensor_id1,))
    
    conn.commit()
    conn.close()
    print("Données test insérées (avec salle)")

if __name__ == "__main__":
    create_tables()
    insert_test_data()
