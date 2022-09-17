import os
import pymongo
import requests
import sys

solax_url = os.environ["SOLAX_URL"]
solax_token_id = os.environ["SOLAX_TOKEN_ID"]
solax_sn = os.environ["SOLAX_SN"]
mongo_cluster = os.environ["MONGO_CLUSTER"]
mongo_username = os.environ["MONGO_USERNAME"]
mongo_password = os.environ["MONGO_PASSWORD"]


def get_mongo_client(mongo_cluster, mongo_username, mongo_password):
    uri = 'mongodb+srv://' + mongo_username + \
        ':' + mongo_password + '@' + mongo_cluster + '?ssl=true&ssl_cert_reqs=CERT_NONE'
    return pymongo.MongoClient(uri)


def get_solax_response(solax_url, solax_token_id, solax_sn):
    solax_url = f"{solax_url}?tokenId={solax_token_id}&sn={solax_sn}"
    response = requests.get(solax_url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Could not fetch Solax data:")
        print("Status code: " + response.status_code)
        print("Status code: " + response.json())
        sys.exit(0)


def insert_record(mongo_client, database_name, collection_name, record):
    db = mongo_client[database_name]
    collection = db[collection_name]
    result = collection.insert_one(record)
    return result


def main():
    client = get_mongo_client(mongo_cluster, mongo_username, mongo_password)
    if client.server_info()["ok"] == 1:
        solax_response = get_solax_response(
            solax_url, solax_token_id, solax_sn)
        result = insert_record(client, 'readings', 'solax', solax_response)
        if result.acknowledged is True:
            print("Inserted object id: " + str(result.inserted_id))
        else:
            print("Could not insert record:")
            sys.exit(0)
    else:
        print("Could not connect to mongo db:")
        print(client.server_info())
        sys.exit(0)


if __name__ == "__main__":
    main()
