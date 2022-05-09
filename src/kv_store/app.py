from ast import Store
from flask import Flask
from interfaces.endpoints import get_kv_store, kv_store_app

app = Flask('kv_store')


@app.route('/')
def hello():
    return "Hello World"


@app.route('/_reset')
def reset():
    store = get_kv_store()
    store.reset()
    return "Done"


get_kv_store()  #  we instantiate the store here before app start so we can ensure it is the same across all threads (mod_wsgi will usually fork on app.run)
                #  this only really matters because we are using a local memory store for the entire app, which normally we would not in production

app.register_blueprint(kv_store_app, url_prefix='/v1')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
