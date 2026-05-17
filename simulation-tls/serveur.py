import paho.mqtt.client as mqtt
import json
import base64
import os
import time
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from crypto.crypto import encrypt_aes, decrypt_aes, compute_sha1, decrypt_rsa

# Configuration MQTT
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
TOPIC_CLIENTS = "clients/requests"      # Les clients envoient ici
TOPIC_SERVER = "server/responses"       # Le serveur repond ici

# Catalogue de produits (code en dur comme demande)
catalogue = [
    {"id": 1, "nom": "Souris USB", "prix": 25},
    {"id": 2, "nom": "Clavier AZERTY", "prix": 45},
    {"id": 3, "nom": "Ecran 24 pouces", "prix": 180},
    {"id": 4, "nom": "Cle USB 32Go", "prix": 15},
    {"id": 5, "nom": "Disque Dur 1To", "prix": 60},
    {"id": 6, "nom": "Carte Graphique", "prix": 350},
    {"id": 7, "nom": "Processeur i5", "prix": 220},
    {"id": 8, "nom": "Barrette RAM 8Go", "prix": 40},
    {"id": 9, "nom": "Casque Audio", "prix": 55},
    {"id": 10, "nom": "Webcam HD", "prix": 35}
]

# Variables globales pour stocker les cles de session par client
session_keys = {}  # Format: {cli_id: session_key}
connected_clients = []  # Liste des clients connectes

def load_server_keys():
    """Charge la cle privee du serveur depuis le fichier PEM"""
    with open("server_private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )
    return private_key

def load_server_cert():
    """Charge le certificat serveur pour l'envoyer aux clients"""
    with open("server_certificate.pem", "rb") as cert_file:
        cert_data = cert_file.read()
    return cert_data

def on_connect(client, userdata, flags, rc):
    """Callback quand le serveur se connecte au broker MQTT"""
    if rc == 0:
        print("[SERVEUR] Connecte au broker MQTT !")
        # S'abonner au topic des clients pour recevoir leurs requetes
        client.subscribe(TOPIC_CLIENTS)
        print(f"[SERVEUR] Abonne au topic: {TOPIC_CLIENTS}")
    else:
        print(f"[SERVEUR] Echec de connexion, code: {rc}")

def on_message(client, userdata, msg):
    """Callback quand un message MQTT est recu"""
    global session_keys, connected_clients

    try:
        # Decoder le message JSON recu
        payload = json.loads(msg.payload.decode('utf-8'))
        msg_type = payload.get("type")
        cli_id = payload.get("cli_id")

        print(f"\n[SERVEUR] Message recu de {cli_id} - Type: {msg_type}")

        if msg_type == "HELLO":
            # Etape 1: Le client demande une connexion
            print(f"[SERVEUR] Demande de connexion de {cli_id}")

            # Envoyer le certificat au client
            cert_data = load_server_cert()
            response = {
                "type": "CERT",
                "certificate": base64.b64encode(cert_data).decode('utf-8')
            }
            client.publish(TOPIC_SERVER, json.dumps(response))
            print(f"[SERVEUR] Certificat envoye a {cli_id}")

        elif msg_type == "KEY_EXCHANGE":
            # Etape 2: Le client envoie la cle de session chiffree avec RSA
            print(f"[SERVEUR] Reception de la cle de session de {cli_id}")

            encrypted_key = base64.b64decode(payload.get("encrypted_key"))

            # Dechiffrer la cle de session avec la cle privee RSA
            private_key = load_server_keys()
            session_key = decrypt_rsa(encrypted_key, private_key)

            if session_key:
                session_keys[cli_id] = session_key
                connected_clients.append(cli_id)
                print(f"[SERVEUR] Cle de session recue et dechiffree pour {cli_id}")
                print(f"[SERVEUR] Cle (hex): {session_key.hex()[:32]}...")

                # Envoyer une confirmation au client
                response = {
                    "type": "KEY_OK",
                    "message": "Cle de session etablie avec succes"
                }
                # Chiffrer la reponse avec AES
                iv = os.urandom(16)
                resp_json = json.dumps(response).encode('utf-8')

                # Calculer le hash SHA-1 SUR LE TEXTE EN CLAIR avant chiffrement
                resp_hash = compute_sha1(resp_json)

                encrypted_resp = encrypt_aes(resp_json, session_key, iv)

                final_resp = {
                    "type": "KEY_OK",
                    "iv": base64.b64encode(iv).decode('utf-8'),
                    "encrypted_data": base64.b64encode(encrypted_resp).decode('utf-8'),
                    "hash": base64.b64encode(resp_hash).decode('utf-8')
                }
                client.publish(TOPIC_SERVER, json.dumps(final_resp))
                print(f"[SERVEUR] Confirmation chiffree envoyee a {cli_id}")
            else:
                print("[SERVEUR] ERREUR: Impossible de dechiffrer la cle de session")

        elif msg_type == "REQUEST":
            # Etape 3: Le client fait une requete (catalogue ou achat)
            print(f"[SERVEUR] Requete de {cli_id}")

            if cli_id not in session_keys:
                print(f"[SERVEUR] ERREUR: Pas de session etablie pour {cli_id}")
                return

            session_key = session_keys[cli_id]

            # Dechiffrer le message du client
            iv = base64.b64decode(payload.get("iv"))
            encrypted_data = base64.b64decode(payload.get("encrypted_data"))
            received_hash = base64.b64decode(payload.get("hash"))

            decrypted_req = decrypt_aes(encrypted_data, session_key, iv)
            if not decrypted_req:
                return

            # Verifier l'integrite SUR LE TEXTE EN CLAIR apres dechiffrement
            if compute_sha1(decrypted_req) != received_hash:
                print("[SERVEUR] ERREUR: Integrite du message compromis !")
                return

            request = json.loads(decrypted_req.decode('utf-8'))
            req_type = request.get("action")

            print(f"[SERVEUR] Requete de type: {req_type}")

            response_data = {}

            if req_type == "GET_CATALOG":
                # Envoyer le catalogue
                response_data = {
                    "type": "CATALOG",
                    "products": catalogue
                }
                print(f"[SERVEUR] Envoi du catalogue ({len(catalogue)} produits)")

            elif req_type == "BUY":
                # Traiter un achat
                prod_id = request.get("product_id")
                quantity = request.get("quantity", 1)

                # Chercher le produit
                product = next((p for p in catalogue if p["id"] == prod_id), None)

                if product:
                    total = product["prix"] * quantity
                    response_data = {
                        "type": "BUY_OK",
                        "message": "Achat reussi !",
                        "product": product["nom"],
                        "quantity": quantity,
                        "total": total
                    }
                    print(f"[SERVEUR] Achat valide: {product['nom']} x{quantity} = {total}€")
                else:
                    response_data = {
                        "type": "BUY_ERROR",
                        "message": "Produit non trouve"
                    }
                    print(f"[SERVEUR] Erreur: Produit {prod_id} non trouve")

            # Chiffrer et envoyer la reponse
            iv = os.urandom(16)
            resp_json = json.dumps(response_data).encode('utf-8')

            # Calculer le hash SHA-1 SUR LE TEXTE EN CLAIR avant chiffrement
            resp_hash = compute_sha1(resp_json)

            encrypted_resp = encrypt_aes(resp_json, session_key, iv)

            final_resp = {
                "type": "RESPONSE",
                "iv": base64.b64encode(iv).decode('utf-8'),
                "encrypted_data": base64.b64encode(encrypted_resp).decode('utf-8'),
                "hash": base64.b64encode(resp_hash).decode('utf-8')
            }
            client.publish(TOPIC_SERVER, json.dumps(final_resp))
            print(f"[SERVEUR] Reponse chiffree envoyee a {cli_id}")

    except Exception as e:
        print(f"[SERVEUR] Erreur lors du traitement: {e}")

def main():
    """Fonction principale du serveur"""
    print("=" * 60)
    print("   SERVEUR VENDEUR - Simulation de vente securisee")
    print("=" * 60)
    print(f"Broker MQTT: {MQTT_BROKER}:{MQTT_PORT}")
    print(f"Catalogue: {len(catalogue)} produits")
    print("=" * 60)

    # Verifier que les fichiers de cles existent
    if not os.path.exists("server_private_key.pem"):
        print("\n[ATTENTION] Fichiers de cles non trouves !")
        print("Veuillez d'abord executer: python gen_keys.py")
        return

    # Creer le client MQTT
    server = mqtt.Client(client_id="VendeurServeur")
    server.on_connect = on_connect
    server.on_message = on_message

    try:
        # Connexion au broker
        print("\n[SERVEUR] Connexion au broker MQTT...")
        server.connect(MQTT_BROKER, MQTT_PORT, 60)

        # Boucle infinie pour ecouter les messages
        print("[SERVEUR] En attente de clients...\n")
        server.loop_forever()

    except KeyboardInterrupt:
        print("\n[SERVEUR] Arret du serveur...")
    except Exception as e:
        print(f"\n[SERVEUR] Erreur: {e}")
        print("Verifiez que le broker Mosquitto est lance !")

if __name__ == "__main__":
    main()
