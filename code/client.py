import requests
import json

base_url = 'https://localhost:5000'
def add_acl1():
    endpoint = '/acl'
    url = base_url + endpoint
    data = {
        "object": "doc:readme",
        "relation": "viewer",
        "user": "user:bob"
    }
    response = requests.post(url, json=data, verify=False)
    print("Add ACL status code: " + str(response.status_code))
    print(data)
    print("Add ACL response: " + str(response.json()))

def add_acl2():
    endpoint = '/acl'
    url = base_url + endpoint
    data = {
        "object": "doc:readme",
        "relation": "editor",
        "user": "user:bob"
    }
    response = requests.post(url, json=data, verify=False)
    print("Add ACL status code: " + str(response.status_code))
    print(data)
    print("Add ACL response: " + str(response.json()))


def check_acl1():
    endpoint = '/acl/check'
    url = base_url + endpoint
    params = {
        'object': 'doc:readme',
        'relation': 'viewer',
        'user': 'user:bob'
    }
    response = requests.get(url, params=params, verify=False)

    print("Check ACL status code: " + str(response.status_code))
    print(params)
    print("Check ACL response: " + str(response.json()))

def check_acl2():
    endpoint = '/acl/check'
    url = base_url + endpoint
    params = {
        'object': 'doc:readme',
        'relation': 'editor',
        'user': 'user:bob'
    }
    response = requests.get(url, params=params, verify=False)

    print("Check ACL status code: " + str(response.status_code))
    print(params)
    print("Check ACL response: " + str(response.json()))

def check_acl22():
    endpoint = '/acl/check'
    url = base_url + endpoint
    params = {
        'object': 'doc:readme',
        'relation': 'viewer',
        'user': 'user:bob'
    }
    response = requests.get(url, params=params, verify=False)

    print("Check ACL status code: " + str(response.status_code))
    print(params)
    print("Check ACL response: " + str(response.json()))

def check_acl222():
    endpoint = '/acl/check'
    url = base_url + endpoint
    params = {
        'object': 'doc:readme',
        'relation': 'owner',
        'user': 'user:bob'
    }
    response = requests.get(url, params=params, verify=False)

    print("Check ACL status code: " + str(response.status_code))
    print(params)
    print("Check ACL response: " + str(response.json()))

def check_acl11():
    endpoint = '/acl/check'
    url = base_url + endpoint
    params = {
        'object': 'doc:readme',
        'relation': 'owner',
        'user': 'user:bob'
    }
    response = requests.get(url, params=params, verify=False)

    print("Check ACL status code: " + str(response.status_code))
    print(params)
    print("Check ACL response: " + str(response.json()))

def add_namespace():
    endpoint = '/namespace'
    url = base_url + endpoint
    data = {
        "namespace": "doc",
        "relations": {
            "owner": {},
            "editor": {
                "union": [
                    {"this": {}},
                    {"computed_userset": {"relation": "owner"}}
                ]
            },
            "viewer": {
                "union": [
                    {"this": {}},
                    {"computed_userset": {"relation": "editor"}}
                ]
            }
        }
    }
    response = requests.post(url, json=data, verify=False)
    print("Add namespace status code: " + str(response.status_code))
    print("Add namespace response: " + str(response.json()))

if __name__ == '__main__':
    add_namespace()
    print("--------------------------------------------------------------")
    add_acl1()
    print("--------------------------------------------------------------")
    check_acl1()
    print("--------------------------------------------------------------")
    check_acl11()
    print("--------------------------------------------------------------")
    add_acl2()
    print("--------------------------------------------------------------")
    check_acl2()
    print("--------------------------------------------------------------")
    check_acl22()
    print("--------------------------------------------------------------")
    check_acl222()
    print("--------------------------------------------------------------")
