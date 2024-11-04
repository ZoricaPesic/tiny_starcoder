import json
import yaml
import plyvel
from ConsulDBService import ConsulDBService, test_redis_connection,test_redis_key_operations
from flask import Flask, request, jsonify, g
from cryptography.fernet import Fernet
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from logging_config import logger
import re
from OpenSSL import SSL
import atexit


app = Flask(__name__)

# Initialize Flask-Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)





def encrypt_data(data):
    return cipher_suite.encrypt(data)


def decrypt_data(encrypted_data):
    return cipher_suite.decrypt(encrypted_data).decode()


def load_config(yaml_file):
    with open(yaml_file, 'r') as file:
        config = yaml.safe_load(file)
    return config


def get_all_acls():
    all_acls = []
    with db.iterator() as it:
        for key, encrypted_value in it:
            object_name = key.decode('utf-8')
            decrypted_value = decrypt_data(encrypted_value.decode('utf-8'))
            acl = json.loads(decrypted_value)
            acl = [tuple(item) for item in acl]
            for subject, right in acl:
                all_acls.append((object_name, subject, right))
    return all_acls


def get_acl(key):
    all_acls = []
    encrypted_content = db.get(key.encode('utf-8'))
    if encrypted_content:
        value = decrypt_data(encrypted_content)
        acl = json.loads(value)
        all_acls = [tuple(item) for item in acl]
    consul_service.acl_store = all_acls
    return all_acls


def add_acl_entry(object_name, subject, right):
    key = object_name.encode('utf-8')
    entry = (object_name, subject, right)
    acl = []

    existing_acl = db.get(key)
    if existing_acl:
        acl = decrypt_data(existing_acl)
        acl = json.loads(acl)

        for e in acl:
            if e[1] == subject:
                acl.remove(e)
    acl.append(entry)

    encrypted = encrypt_data(json.dumps(acl).encode('utf-8'))
    db.put(key, encrypted)

@app.before_request
def log_request_info():
    logger.info(f"Received {request.method} request for {request.url} from {request.remote_addr}")


@app.route('/acl', methods=['POST'])
@limiter.limit("10 per minute")
def add_acl():

    pattern = re.compile(r'^[a-zA-Z0-9:]+$')
    pattern_user_object = re.compile(r'^[\w\s]*:[\w\s]*$')

    data = request.get_json()
    object = data['object']
    relation = data['relation']
    user = data['user']

    if not pattern_user_object.match(object):
        return jsonify({"status": "Object must be in format namespace:object_id"}), 400

    if not pattern_user_object.match(user):
        return jsonify({"status": "User must be in format user:user_id"}), 400

    if pattern.match(object) and pattern.match(relation) and pattern.match(user):
        add_acl_entry(object, user, relation)
        logger.info(f"Added ACL entry: object={object}, relation={relation}, user={user}")
        return jsonify({"status": "Added new acl entry."}), 200


    return jsonify({"status": "Only letters and numbers are allowed."}), 400



@app.route('/acl/check', methods=['GET'])
@limiter.limit("20 per minute")
def check_acl():
    pattern = re.compile(r'^[a-zA-Z0-9:]+$')
    pattern_user_object = re.compile(r'^[\w\s]*:[\w\s]*$')

    object = request.args.get('object')
    relation = request.args.get('relation')
    user = request.args.get('user')

    if not pattern_user_object.match(object):
        return jsonify({"status": "Object must be in format namespace:object_id"}), 400

    if not pattern_user_object.match(user):
        return jsonify({"status": "User must be in format user:user_id"}), 400

    if pattern.match(object) and pattern.match(relation) and pattern.match(user):
        get_acl(object)
        authorized = consul_service.user_has_role(object, relation, user)
        logger.info(f"Checked ACL: object={object}, relation={relation}, user={user}, authorized={authorized}")
        return jsonify({"authorized": authorized}), 200

    return jsonify({"status": "Only letters and numbers are allowed."}), 400


@app.route('/namespace', methods=['POST'])
@limiter.limit("5 per minute")
def add_namespace():
    pattern = re.compile(r'^[\w:,"[\]{} -]*$')
    data = request.get_json()
    data_str = json.dumps(data)
    print(data_str)
    namespace = data['namespace']

    if pattern.match(data_str):
        consul_service.save_namespace_config(namespace, data)
        logger.info(f"Added namespace: {namespace}")
        return jsonify({"status": "Namespace added"}), 200

    return jsonify({"status": "Only letters and numbers are allowed."}), 400



@app.route('/getAll', methods=['POST'])
def get_all():
    data = request.get_json()
    return jsonify({"status": json.dumps(get_acl(data['object']))}), 200


config = load_config('config.yaml')
db = plyvel.DB(config['leveldb_path'], create_if_missing=True, lru_cache_size=8_000_000)

CERT_FILE = config["flask_cert"]
KEY_FILE = config["flask_key"]

context = SSL.Context(SSL.TLSv1_2_METHOD)
context.use_certificate_file(CERT_FILE)
context.use_privatekey_file(KEY_FILE)

consul_service = ConsulDBService(config)
namespace = "doc"
test_redis_connection(config['redis_host'], config['redis_port'])
test_redis_key_operations(config['redis_host'], config['redis_port'])
key = config["key"]
if key:
    cipher_suite = Fernet(key)


def cleanup():
    db.close()

atexit.register(cleanup)
