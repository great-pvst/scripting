import paho.mqtt.client as mqtt
import json
import base64
import os
import time
import random
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography import x509
from crypto.crypto import encrypt_rsa, encrypt_aes, decrypt_aes, compute_sha1, load_server_certificate

# Configuration MQTT
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
TOPIC_CLIENTS = "clients/requests"
TOPIC_SERVER = "server/responses"

# Variables globales
session_key = None  # Cle de session AES partagee avec le serveur
cli_id = None       # ID du client (genere automatiquement)
server_cert = None  # Certificat du serveur recu
catalog_received = False 

def generate_client_id():
    """Genere un ID client aleatoire (C1, C2, etc.)"""
    return f"C{random.randint(1, 99)}"

def on_connect(client, userdata, flags, rc):
    """Callback connexion au broker"""
    if rc == 0:
        print(f"[CLIENT {cli_id}] Connecte au broker MQTT")
        # S'abonner au topic serveur pour recevoir les reponses
        client.subscribe(TOPIC_SERVER)
        print(f"[CLIENT {cli_id}] Abonne au topic: {TOPIC_SERVER}")

        # Etape 1: Envoyer HELLO au serveur
        hello_msg = {
            "type": "HELLO",
            "cli_id": cli_id
        }
        client.publish(TOPIC_CLIENTS, json.dumps(hello_msg))
        print(f"[CLIENT {cli_id}] Message HELLO envoye au serveur")
    else:
        print(f"[CLIENT] Echec connexion: {rc}")

def on_message(client, userdata, msg):
    """Callback reception message du serveur"""
    global session_key, server_cert, catalog_received

    try:
        payload = json.loads(msg.payload.decode('utf-8'))
        msg_type = payload.get("type")

        if not catalog_received:
            print(f"\n[CLIENT {cli_id}] Message recu - Type: {msg_type}")

        if msg_type == "CERT":
            # Etape 2: Recevoir le certificat du serveur
            print(f"[CLIENT {cli_id}] Reception du certificat serveur")

            cert_data = base64.b64decode(payload.get("certificate"))
            cert = load_server_certificate(cert_data)

            if cert:
                server_cert = cert
                print(f"[CLIENT {cli_id}] Certificat serveur recu")
                print(f"[CLIENT {cli_id}] CN: {cert.subject.get_attributes_for_oid(x509.oid.NameOID.COMMON_NAME)[0].value}")

                # Extraire la cle publique du certificat
                public_key = cert.public_key()

                # Generer une cle de session AES-256 aleatoire
                session_key = os.urandom(32)  # 256 bits = 32 bytes
                print(f"[CLIENT {cli_id}] Cle de session AES generee")
                print(f"[CLIENT {cli_id}] Cle (hex): {session_key.hex()[:32]}...")

                # Chiffrer la cle de session avec RSA (cle publique serveur)
                encrypted_key = encrypt_rsa(session_key, public_key)

                if encrypted_key:
                    # Envoyer la cle chiffree au serveur (pas de hash sur la cle RSA car deja secure)
                    key_msg = {
                        "type": "KEY_EXCHANGE",
                        "cli_id": cli_id,
                        "encrypted_key": base64.b64encode(encrypted_key).decode('utf-8')
                    }
                    client.publish(TOPIC_CLIENTS, json.dumps(key_msg))
                    print(f"[CLIENT {cli_id}] Cle de session chiffree avec RSA envoyee")

        elif msg_type == "KEY_OK":
            # Etape 3: Confirmation de la part du serveur
            print(f"[CLIENT {cli_id}] Cle de session confirmee par le serveur")

            if session_key is None:
                print("[CLIENT] ERREUR: Pas de cle de session !")
                return

            # Dechiffrer la reponse
            iv = base64.b64decode(payload.get("iv"))
            encrypted_data = base64.b64decode(payload.get("encrypted_data"))
            received_hash = base64.b64decode(payload.get("hash"))

            # Dechiffrer d'abord
            decrypted = decrypt_aes(encrypted_data, session_key, iv)
            if not decrypted:
                return

            # Verifier integrite SUR LE TEXTE EN CLAIR apres dechiffrement
            if compute_sha1(decrypted) != received_hash:
                print("[CLIENT] ERREUR: Integrite compromis !")
                return

            resp = json.loads(decrypted.decode('utf-8'))
            print(f"[CLIENT {cli_id}] Serveur: {resp.get('message')}")

            # Demander le catalogue
            print(f"\n[CLIENT {cli_id}] Demande du catalogue...")
            send_request(client, "GET_CATALOG")

        elif msg_type == "RESPONSE":
            # Recevoir une reponse du serveur (catalogue ou achat)
            if session_key is None:
                print("[CLIENT] ERREUR: Pas de session etablie !")
                return

            iv = base64.b64decode(payload.get("iv"))
            encrypted_data = base64.b64decode(payload.get("encrypted_data"))
            received_hash = base64.b64decode(payload.get("hash"))

            # Dechiffrer d'abord
            decrypted = decrypt_aes(encrypted_data, session_key, iv)
            if not decrypted:
                return

            # Verifier integrite SUR LE TEXTE EN CLAIR apres dechiffrement
            if compute_sha1(decrypted) != received_hash:
                print("[CLIENT] ERREUR: Integrite compromis !")
                return

            response = json.loads(decrypted.decode('utf-8'))
            resp_type = response.get("type")

            if resp_type == "CATALOG":
                products = response.get("products")
                print(f"\n[CLIENT {cli_id}] CATALOGUE RECU ({len(products)} produits):")
                print("-" * 50)
                for p in products:
                    print(f"  [{p['id']}] {p['nom']:<25} {p['prix']}€")
                print("-" * 50)

                catalog_received = True

            elif resp_type == "BUY_OK":
                print(f"\n[CLIENT {cli_id}] ACHAT VALIDE !")
                print(f"  Produit: {response.get('product')}")
                print(f"  Quantite: {response.get('quantity')}")
                print(f"  Total: {response.get('total')}€")

            elif resp_type == "BUY_ERROR":
                print(f"\n[CLIENT {cli_id}] Erreur achat: {response.get('message')}")

    except Exception as e:
        print(f"[CLIENT] Erreur: {e}")

def send_request(client, action, params=None):
    """Envoie une requete chiffree au serveur"""
    if session_key is None:
        print("[CLIENT] Pas de cle de session !")
        return

    request = {"action": action}
    if params:
        request.update(params)

    # Chiffrer avec AES
    iv = os.urandom(16)
    req_json = json.dumps(request).encode('utf-8')

    # Calculer le hash SHA-1 SUR LE TEXTE EN CLAIR avant chiffrement
    hash_value = compute_sha1(req_json)

    encrypted_req = encrypt_aes(req_json, session_key, iv)

    if encrypted_req:
        msg = {
            "type": "REQUEST",
            "cli_id": cli_id,
            "iv": base64.b64encode(iv).decode('utf-8'),
            "encrypted_data": base64.b64encode(encrypted_req).decode('utf-8'),
            "hash": base64.b64encode(hash_value).decode('utf-8')
        }
        client.publish(TOPIC_CLIENTS, json.dumps(msg))
        print(f"[CLIENT {cli_id}] Requete '{action}' envoyee (chiffree AES)")

def main():
    """Fonction principale du client"""
    global cli_id
    cli_id = generate_client_id()

    print("=" * 60)
    print(f"   CLIENT ACHETEUR - {cli_id}")
    print("=" * 60)
    print(f"Broker MQTT: {MQTT_BROKER}:{MQTT_PORT}")
    print("=" * 60)

    # Creer le client MQTT
    client = mqtt.Client(client_id=cli_id)
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        print(f"\n[CLIENT {cli_id}] Connexion au broker MQTT...")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)

        client.loop_start()

        while not catalog_received:
            time.sleep(0.5)

        while True:
            time.sleep(0.5)
            print("\n1. Acheter un produit")
            print("2. Quitter")
            choix = input("Choix (1/2) : ")

            if choix == "1":
                try:
                    prod_id = int(input("ID du produit : "))
                    qte = int(input("Quantite : "))
                    send_request(client, "BUY", {"product_id": prod_id, "quantity": qte})
                except ValueError:
                    print("Saisie invalide.")
            elif choix == "2":
                break

        client.loop_stop()
        client.disconnect()

    except KeyboardInterrupt:
        print(f"\n[CLIENT {cli_id}] Deconnexion...")
        client.loop_stop()
        client.disconnect()
    except Exception as e:
        print(f"\n[CLIENT] Erreur: {e}")
        print("Verifiez que le broker Mosquitto est lance !")

if __name__ == "__main__":
    main()