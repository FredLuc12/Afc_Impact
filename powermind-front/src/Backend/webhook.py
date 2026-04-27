import requests


def send_make_webhook(capteur_type, valeur, seuil, message):
    webhook_url = "https://hook.eu1.make.com/y5skp23xpqt5g200bp2ikorbapk5sjob"

    payload = {
        "alerte": {
            "type": capteur_type,
            "valeur": float(valeur),
            "seuil": float(seuil),
            "message": message,
        }
    }
    
    try:
        r = requests.post(webhook_url, json=payload, timeout=10)
        print(f"Webhook OK: {r.status_code}")
        return True
    except Exception as e:
        print(f"Webhook erreur: {e}")
        return False
