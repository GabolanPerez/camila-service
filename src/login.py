from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

conexion=MySQL(app)

# Se añaden los en general todos los CORS
CORS(app, origins="*")    

def login_getUser(username, password):
    try:
        cursor = conexion.connection.cursor()
        sql="SELECT * FROM usuario WHERE USER_NAME = '{0}' AND PASSWORD = '{1}' ".format(username, password)
        cursor.execute(sql)
        datos = cursor.fetchone()
        print(datos)
        if datos != None:
            user={'id':datos[0],'nombre':datos[3],'paterno':datos[1],'materno':datos[2],'email':datos[4],'username':datos[5],'password':datos[6], 'status':("Inactivo", "Activo")[int.from_bytes(datos[7],byteorder='big')]}
            return user
        else:
            return None
    except Exception as ex:
        raise ex

@app.route('/login', methods=['GET'])
def login():

    username = request.args.get('username')
    password = request.args.get('password')
    try:
        user = login_getUser(username, password)
        if user == None:
            return jsonify({'mensaje':"Usuario no encontrado.", 'exito':False})
        else:
            return jsonify({'user':user, 'mensaje':"Usuario encontrado", 'exito':True})
    
    except Exception as ex:
        return jsonify({'mensaje':"Error"})
    

@app.route('/userslogin/<username>/<password>', methods=['GET'])
def login_user(username, password):
    try:
        print(username, "   ", password)
        user = username
        if user == None:
            return jsonify({'mensaje':"Usuario no encontrado.", 'exito':False})
        elif user == "Usuario encontrado con estatus inactivo.":
            return jsonify({'mensaje':user, 'exito':False})
        else:
            # user={'Id':datos[0],'Nombre':datos[3],'Paterno':datos[1],'Materno':datos[2],'Email':datos[4],'Usuario':datos[5],'Password':datos[6]}
            return jsonify({'user':user, 'mensaje':"Usuario encontradsso", 'exito':True})
    
    except Exception as ex:
        return jsonify({'mensaje':"Error"})
    

def pagina_no_necontrada(error):
    return "<h1>La página que intentas buscar, no existe....</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_necontrada)
    app.run()

