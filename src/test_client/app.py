from flask import Flask
import requests
import json
import logging
from typing import List


app = Flask('kv_store_test')
logger = app.logger


def get_store_app_port():
    import os
    return int(os.environ.get('STORE_PORT', 8080))


def get_store_app_hostname():
    import os
    return str(os.environ.get('STORE_CONTAINER', '127.0.0.1'))


def get_host_url():
    return f"http://{get_store_app_hostname()}:{get_store_app_port()}/"


def make_request(endpoint, data, request_func):
    headers = {"Content-Type": "application/json"}
    url, data = get_host_url() + endpoint, json.dumps(data)
    logger.info(f"Calling api - Url: {url} Headers: {headers} Data: {data} Type: {request_func.__name__}")
    response = request_func(url=url, data=data, headers=headers)
    logger.info(f"Api response - Status: {response.status_code}, Content: {response.content}")
    return response


def get_key(keyname):
    ret = make_request(f"v1/{keyname}", {}, requests.get)
    content = json.loads(ret.content) if ret.status_code == 200 else {"value": None}
    return ret.status_code, content['value']


def reset_store():
    return make_request("_reset", {}, requests.get)


def set_key_post(keyname, value):
    return make_request(f"v1/", {"key": keyname, "value": value}, requests.post).status_code


def set_key_put(keyname, value):
    return make_request(f"v1/{keyname}", {"value": value}, requests.put).status_code


def delete_key(keyname):
    return make_request(f"v1/{keyname}", {}, requests.delete).status_code


@app.route('/')
def hello():
    return "Hello World"


@app.route('/test_deletion')
def delete():
    reset_store()
    messages = []
    try:
        message_and_log("Building base keyset:", messages)
        assert set_key_put('1', 'bara') == 200
        assert set_key_put('2', 'barb') == 200
        assert set_key_put('3', 'barc') == 200
        assert set_key_put('4', 'bard') == 200
        assert set_key_put('5', 'bare') == 200
        assert set_key_put('6', 'barf') == 200
        assert set_key_put('7', 'barg') == 200
        assert set_key_put('8', 'barh') == 200
        assert set_key_put('9', 'bari') == 200
        assert set_key_put('10', 'barj') == 200
        message_and_log("Done", messages)

        message_and_log("Testing delete:", messages)
        assert delete_key('1') == 200
        assert delete_key('1') == 404
        assert get_key('1') == (404, None)
        message_and_log("Passed", messages)

        message_and_log("Testing delete, create, delete:", messages)
        assert delete_key('2') == 200
        assert get_key('2') == (404, None)
        assert set_key_put('2', 'bark') == 200
        assert get_key('2') == (200, 'bark')
        assert delete_key('2') == 200
        assert get_key('2') == (404, None)

        message_and_log("Passed", messages)


        message_and_log("Deleteing and testing all keys", messages)
        assert delete_key('1') == 404
        assert delete_key('2') == 404
        assert delete_key('3') == 200
        assert delete_key('4') == 200
        assert delete_key('5') == 200
        assert delete_key('6') == 200
        assert delete_key('7') == 200
        assert delete_key('8') == 200
        assert delete_key('9') == 200
        assert delete_key('10') == 200
        assert get_key('1') == (404, None)
        assert get_key('2') == (404, None)
        assert get_key('3') == (404, None)
        assert get_key('4') == (404, None)
        assert get_key('5') == (404, None)
        assert get_key('6') == (404, None)
        assert get_key('7') == (404, None)
        assert get_key('8') == (404, None)
        assert get_key('9') == (404, None)
        assert get_key('10') == (404, None)
        message_and_log("Passed", messages)
    except Exception as e:
        messages.extend(['', '', "FAILED - Aborting"])


    return '<br>'.join(messages)


def message_and_log(message, messages: List):
    logger.info(message)
    messages.append(message)

@app.route('/test_overwrite')
def overwrite():
    reset_store()
    messages = []
    try:
        message_and_log("Building base keyset:", messages)
        assert set_key_put('5', 'bar') == 200
        assert set_key_put('6', 'bara') == 200
        assert set_key_put('7', 'barb') == 200
        message_and_log('passed', messages)

        message_and_log("testing basic put overwrite:", messages)
        assert set_key_put('5', 'barc') == 200
        assert get_key('5') == (200, 'barc')
        message_and_log("passed", messages)
        message_and_log("Testing post works but does not overwrite:", messages)
        assert set_key_post('6', 'bar') == 409
        assert set_key_post('8', 'bar') == 200
        assert get_key('6') == (200, 'bara')
        assert get_key('8') == (200, 'bar')
        message_and_log("passed", messages)
        message_and_log("Testing multiple overwrites of the same key:", messages)
        assert set_key_put('7', 'bara') == 200
        assert set_key_put('7', 'barb') == 200
        assert set_key_put('7', 'barc') == 200
        assert set_key_put('7', 'bard') == 200
        assert set_key_put('7', 'bare') == 200
        assert set_key_put('7', 'barf') == 200
        assert set_key_put('7', 'barg') == 200
        assert set_key_put('7', 'barh') == 200
        assert set_key_put('7', 'bari') == 200
        assert set_key_put('7', 'barj') == 200
        assert get_key('7') == (200, 'barj')
        message_and_log("passed", messages)

    except Exception:
        messages.append(['', '', "FAILED - Aborting"])

    return '<br>'.join(messages)



logger.setLevel(logging.INFO)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
