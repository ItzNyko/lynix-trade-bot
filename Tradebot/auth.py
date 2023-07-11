import requests
from utils import *
from Crypto.PublicKey import *
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


"""
Authentication System 2.0 bc poky did this 


Client side generates key pair and stores private key
Client side gets public key from server 
Client side gets its public_key 
Client side posts its public key, encrypted data with server's public key
Server side sends encrypted response with client's public key
Client compares data
"""

SERVER_CREATE_KEY = "https://nykolynix.herokuapp.com/createkey"
SERVER_CHECK_AUTH = "https://nykolynix.herokuapp.com/nina"

client_key_pairs = {}


def client_generate_key_pair() -> bytes:
    """
    Returns RSA key pair used further in Authentication system. Returns client-side public_key
    Accessed with client_key_pairs[public_key] = private_key
    """
    key_pair = RSA.generate(1024)  # 3072)
    client_key_pairs[
        key_pair.public_key().exportKey().hex()
    ] = key_pair.exportKey().hex()

    return key_pair.public_key().exportKey().hex()


def client_encrypt(public_key: str, content: str) -> bytes:
    """
    (CLIENT-SIDED) Encrypts msg using public key given by server
    """

    return (
        PKCS1_OAEP.new(RSA.import_key(bytes.fromhex(public_key)))
        .encrypt(bytes(content, "UTF-8"))
        .hex()
    )


def client_decrypt(private_key: bytes, content: bytes) -> str:
    """
    (CLIENT-SIDED) modified version of server sided decryption, instead requiring private key
    """
    try:
        return (
            PKCS1_OAEP.new(RSA.import_key(bytes.fromhex(private_key)))
            .decrypt(bytes.fromhex(content))
            .decode("UTF-8")
        )
    except:
        return ""


def check_authentication(user_id: int) -> bool:
    try:
        """
        Returns whether user is authenticated
        """
        client_public_key = client_generate_key_pair()
        client_private_key = client_key_pairs[client_public_key]
        server_public_key = requests.get(SERVER_CREATE_KEY).json()
        encrypted_data = client_encrypt(server_public_key, str(user_id))
        data = {
            "server_public_key": server_public_key,
            "client_public_key": client_public_key,
            "client_data": encrypted_data,
        }
        try:
            response = requests.post(SERVER_CHECK_AUTH, json=data).json()
        except:
            return False
        if (
            client_decrypt(client_private_key, response)
            == str(user_id) + " IS AUTHENTICATED"
        ):
            del client_key_pairs[client_public_key]
            return True
        return False
    except:
        return False


def auth_thread(user_id: int, wait_time: int):
    """
    Authentication thread check for user_id
    """
    while True:
        time.sleep(10)
        if not check_authentication(user_id):
            print("User is not authenticated!")
            exit(-1)
