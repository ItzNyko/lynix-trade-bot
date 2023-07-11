from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import Crypto
import time
import json

key_pairs = {}
AUTHENTICATED_USER_IDS = [1530946960]


def check_keys():
    """
    Removes oldest key after X seconds to prevent overloads
    """
    while True:
        if len(key_pairs) > 0:
            try:
                time.sleep(35)
                key_pairs.pop(list(key_pairs.keys())[0])
                print("Successfully expired old key!")
            except:
                pass


class authentication:
    def server_create_key() -> bytes:
        """
        Creates RSA public/private key pair and returns hexed public_key to send to client (Server-sided)
        STORED AS: key_pairs[publicKey] = privateKey
        """
        key_pair = RSA.generate(1024)  # 3072
        key_pairs[key_pair.public_key().exportKey().hex()] = key_pair.exportKey().hex()
        return key_pair.public_key().exportKey().hex()

    def server_decrypt(private_key: str, content: bytes) -> str:
        """
        (SERVER-SIDED) Decrypts msg into string, requiring public key to access full keyPair
        publicKey is given to client, after calling create_key(), it is reused in this process
        """
        return (
            PKCS1_OAEP.new(RSA.import_key(bytes.fromhex(private_key)))
            .decrypt(bytes.fromhex(content))
            .decode("UTF-8")
        )

    def server_encrypt(public_key: str, content: str) -> bytes:
        """
        (SERVER-SIDED) Encrypts msg using public key given by server
        """

        return (
            PKCS1_OAEP.new(RSA.import_key(bytes.fromhex(public_key)))
            .encrypt(bytes(content, "UTF-8"))
            .hex()
        )

    def check_authentication(
        server_public_key: str, client_public_key: str, data: bytes
    ):
        """
        (SERVER-SIDED) Returns whether list with [privateKey, response], response contains yes/no if authenticated
        """
        server_private_key = key_pairs[server_public_key]
        decrypted_data = int(authentication.server_decrypt(server_private_key, data))
        if decrypted_data in AUTHENTICATED_USER_IDS:
            print(str(decrypted_data) + " was authenticated!")
            return_data = authentication.server_encrypt(
                client_public_key, str(decrypted_data) + " IS AUTHENTICATED"
            )
            del key_pairs[server_public_key]
            return json.dumps(return_data)
        else:
            print(str(decrypted_data) + " is not authenticated!")
            return "where is nina lowkey? (USER NOT AUTHENTICATED)"
