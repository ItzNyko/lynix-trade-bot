from flask import Flask, request, json
import time
import threading
import proxies
import server_auth
import server_rolimons
import server_datagen
import server_proj

from Crypto import *

app = Flask(__name__)


def rolimon_update_thread():
    while True:
        server_rolimons.refresh_data()
        time.sleep(1000)


print("Starting Lynix backend...")
proxies.parse_proxies()
key_thread = threading.Thread(target=server_auth.check_keys)
key_thread.start()
print("Created key checking thread!")
roli = threading.Thread(target=rolimon_update_thread)
roli.start()
print("Created rolimons updating thread!")
proje = threading.Thread(target=server_datagen.generation_thread)
proje.start()
print("Created datagen thread!")
print(server_proj.calculated_item_data(2470988022))
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


# APIs:


@app.route("/itemdata", methods=["GET"])
def show_projected_items():
    if request.method == "GET":
        return json.dumps(server_datagen.data_values)


@app.route("/createkey", methods=["GET"])
def show_key():
    if request.method == "GET":
        return json.dumps(str(server_auth.authentication.server_create_key()))


@app.route("/nina", methods=["POST"])
def check_auth():
    if request.method == "POST":
        json_data = request.json
        server_public_key = json_data["server_public_key"]
        client_public_key = json_data["client_public_key"]
        client_data = json_data["client_data"]
        return server_auth.authentication.check_authentication(
            server_public_key, client_public_key, client_data
        )
