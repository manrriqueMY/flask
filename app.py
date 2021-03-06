from flask import Flask, request, send_from_directory
# from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from random import randrange
from flask_cors import CORS

app = Flask(__name__, static_url_path='')
# app.config["MONGO_URI"] = "mongodb://localhost:27017/dbtest"
# app.config["MONGO_URI"] = "mongodb://root:1PxK1vVvU2EGPgtd@cluster0-shard-00-00.trhtt.mongodb.net:27017,cluster0-shard-00-01.trhtt.mongodb.net:27017,cluster0-shard-00-02.trhtt.mongodb.net:27017/dbtest?ssl=true&replicaSet=atlas-bz5wrp-shard-0&authSource=admin&retryWrites=true&w=majorit"
# mongo = PyMongo(app)
mongo = MongoClient(
    "mongodb+srv://root:1PxK1vVvU2EGPgtd@cluster0.trhtt.mongodb.net/test?retryWrites=true&w=majority")
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/static/image/<path:path>')
def send_js(path):
    return send_from_directory('static/image', path)


class User(object):
    def __init__(self, _id, id, username, password):
        self._id = _id
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "%s" % self.id


def authenticate(username, password):
    user = mongo.db.users.find_one({"username": username})
    if user and safe_str_cmp(user['password'].encode('utf-8'), password.encode('utf-8')):
        return User(user['_id'], user['id'], user['username'], user['password'])


def identity(payload):
    print(payload)
    user_id = payload['identity']
    # return userid_table.get(user_id, None)
    user = mongo.db.users.find_one({"id": user_id})
    return User(user['_id'], user['id'], user['username'], user['password'])


@app.route('/api/v1/puntuation')
@jwt_required()
def gpuntuation():
    data = list(mongo.db.puntuations.find({"_id": str(current_identity.id)}))
    if(len(data) > 0):
        return {"status_code": "200", "data": data[0]}
    else:
        return {"status_code": "200", "data": {"_id": str(current_identity.id), "puntuacion": 0, "tiempo": "00:00:00"}}


@app.route('/api/v1/puntuation', methods=["POST"])
@jwt_required()
def puntuation():
    data = list(mongo.db.puntuations.find({"_id": str(current_identity.id)}))
    puntos = request.get_json()

    if(len(data) > 0):
        mongo.db.puntuations.update({"_id": str(current_identity.id)}, {
            "$set": {"puntuacion": puntos["puntuacion"], "tiempo": puntos["tiempo"], "username": str(current_identity.username)}})
    else:
        mongo.db.puntuations.insert(
            {"_id": str(current_identity.id), "puntuacion": puntos["puntuacion"], "tiempo": puntos["tiempo"], "username": str(current_identity.username)})
        data = [{"_id": str(current_identity.id),
                 "puntuacion": puntos["puntuacion"]}]

    return {"status_code": "200", "data": data[0]}


@ app.route("/api/v1/register", methods=["POST"])
def register():
    data = request.get_json()
    user = list(mongo.db.users.find({"username": data['username']}))
    if(len(user) > 0):
        return {"status_code": "401", "error": "username is used", "description": "this user is already existed"}

    mongo.db.users.insert(
        {"id": str(randrange(1000)), "username": data['username'], "password": data['password']})
    return {"status_code": "200", "data": request.get_json()}


@ app.route("/api/v1/user")
@ jwt_required()
def guser():
    data = mongo.db.users.find({"id": current_identity.id})
    data = list(data)
    if(len(data) > 0):
        return {"status_code": "200", "data": {"id": data[0]['id'], "username": data[0]['username'], "password": data[0]['password']}}
    else:
        return {"status_code": "401", "error": "user is nos exist", "description": "this user has been removed"}


@ app.route("/index")
@ app.route("/")
def index():
    return {"status_code": "200", "data": {"index": "index"}}


@ app.route("/api/v1/questions")
def questions():
    data = mongo.db.questions.find({})
    data = list(data)
    return {"status_code": "200", "data": data}


@ app.route("/api/v1/leaderboard")
def leaderboard():
    data = mongo.db.puntuations.find({}).sort(
        [("puntuacion", -1), ("tiempo", 1)])
    data = list(data)
    return {"status_code": "200", "data": data}


app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = False
jwt = JWT(app, authenticate, identity)
if __name__ == "__main__":
    app.run(debug=True)
