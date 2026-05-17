from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography import x509
from cryptography.x509.oid import NameOID
import datetime

print("Generation des cles et certificats...")

# Generation de la cle privee RSA 2048 bits pour le serveur
print("-> Creation de la cle RSA 2048 bits...")
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Sauvegarder la cle privee
with open("server_private_key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ))

# Sauvegarder la cle publique
public_key = private_key.public_key()
with open("server_public_key.pem", "wb") as f:
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ))

# Creation du certificat X.509 auto-signe
print("-> Creation du certificat X.509 auto-signe...")
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "FR"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Ile-de-France"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Paris"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Projet TLS"),
    x509.NameAttribute(NameOID.COMMON_NAME, "VendeurServeur"),
])

cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    public_key
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.utcnow()
).not_valid_after(
    datetime.datetime.utcnow() + datetime.timedelta(days=365)
).add_extension(
    x509.SubjectAlternativeName([x509.DNSName("localhost")]),
    critical=False,
).sign(private_key, hashes.SHA256())

# Sauvegarder le certificat
with open("server_certificate.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print("Termine !")
print("Fichiers crees :")
print("  - server_private_key.pem (cle privee serveur)")
print("  - server_public_key.pem (cle publique serveur)")
print("  - server_certificate.pem (certificat X.509)")
