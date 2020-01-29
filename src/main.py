"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, User, Task
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "task": "Alguna tarea",
        "done": "true"
    }

    return jsonify(response_body), 200

@app.route('/todos/user/<username>', methods=['POST', 'GET','PUT','DELETE'])
def handle_user_task(username):

    headers = {
        "Content-Type": "application/json"
    }
    #Chequeando si el usuario existe
    requesting_user = User.query.filter_by(username=username).all()
    if len(requesting_user) > 0:
        username_id = requesting_user[0].id
    else : 
        username_id = None 

    if request.method == 'GET':
        
        print("Hello, GET!")
        if username_id is not None:
            # Existe el usuario, retornamos la lista de tareas...
            print("Usuario Existe")
            user_tasks_list = Task.query.filter_by(user_id=username_id).all()
            response_body = []
            for task in user_tasks_list:
                response_body.append(task.serialize())
            status_code = 200
        else :
            print("Usuario No Existe")
            response_body = {
                "status" : "HTTP_404_NOT_FOUND. Usuario no existe"
            }
            status_code = 404
        
    elif request.method == 'POST':
        
        print("Creando Usuario con una tarea")

        if username_id:
            
            response_body = {
                "status": "HTTP_400_BAD_REQUEST. Usuario ya existe..."
            }
            status_code = 400
        
        elif request.data != []:
            
            response_body = {
                "status": "HTTP_400_BAD_REQUEST. Datos inesperados para crear usuario"
            }
            status_code = 400

        else:
            # username not in use, create user with sample task...
            print("Creando usuario con una tarea")
            new_user = User()
            new_user.username = username
            db.session.add(new_user)
            sample_task = Task("sample task", username_id)
            db.session.add(sample_todo)
            db.session.commit()
            response_body = {
                "status": "Ok"
            }
            status_code = 200

    elif request.method == 'PUT':
        
        # El usuario actualiza la lista completa de tareas, se chequea si existe primerp...
        print(f"updating full list for {username}")

        if username_id:
            # Usuario existe, actualizamos toda la lista...
            # Eliminando tareas existentes...
            Task.query.filter_by(user_id=username_id).delete()
            new_tasks = json.loads(request.data)
            
            for task in new_tasks:
                
                new_task = Task(task["label"], username_id)
                db.session.add(new_task)

            db.session.commit()
            result = f"A list with {len(new_tasks)} todos was succesfully saved"
            response_body = {
                "result": result,
            }
            status_code = 200

        else: 
            # Usuario no exite...
            response_body = {
                "status": "HTTP_400_BAD_REQUEST. No se puede actualizar la lista de un usario inexistente..."
            }
            status_code = 400

    elif request.method == "DELETE":
        # Usuario quiere eliminar si registro y lista...
        if username_id:
            # Usuario existe, eliminando registros...

            Task.query.filter_by(user_id=username_id).delete()
            User.get_by_id(int(username_id)).delete()
            db.session.commit()
            response_body = {
                "result": "ok",
                "status": "HTTP_204_NO_CONTENT. Usuarios Y Tareas Eliminad@s."
            }
            status_code = 204
        
        else:
            # user does not exist, this is a no go...
            response_body = {
                "status": "HTTP_400_BAD_REQUEST. Cannot delete a non existing user..."
            }
            status_code = 400

    else:
        response_body = "Metodo no esta listo todavia"
        status_code = 501

    return make_response(
        jsonify(response_body),
        status_code,
        headers
    )

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
