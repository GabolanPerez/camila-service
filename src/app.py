from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app) #Opción uno habilitar CORS de ruta en ruta

conexion=MySQL(app)

CORS(app, origins="*") #Con esot habilitamos todas las rutas dando permiso a los CORS

# CORS(app, resources={r"/users/*": {"origins": "htpp://localhost"}}) #Habilitando CORS por dominio

def leer_usuario_bd_by_id(id):
    try:
        cursor = conexion.connection.cursor()
        sql="SELECT * FROM usuario WHERE ID = '{0}'".format(id)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            user={'Id':datos[0],'Nombre':datos[3],'Paterno':datos[1],'Materno':datos[2],'Email':datos[4],'Usuario':datos[5],'Password':datos[6], 'Status':("Inactivo", "Activo")[int.from_bytes(datos[7],byteorder='big')]}
            return user
        else:
            return None
    except Exception as ex:
        raise ex
    
def leer_usuario_bd(id = 0, email=None, user_name=None):
    try:
        cursor = conexion.connection.cursor()
        if id != 0:
            print(1)
            sql="SELECT * FROM usuario WHERE ID = '{0}'".format(id)
        elif email != None or user_name != None :
            print(2, email, user_name)
            sql="SELECT * FROM usuario WHERE EMAIL = '{0}' OR USER_NAME = '{1}'".format(email, user_name)
        else:
            print(4)
            sql="SELECT * FROM usuario WHERE ID = '{0}'".format(id)
        
        

        cursor.execute(sql)
        datos = cursor.fetchone()
        print(datos)
        if datos != None:
            if("Inactivo", "Activo")[int.from_bytes(datos[7],byteorder='big')] == "Activo":
                if email == None and user_name == None:
                    user={'Id':datos[0],'Nombre':datos[3],'Paterno':datos[1],'Materno':datos[2],'Email':datos[4],'Usuario':datos[5],'Password':datos[6], 'Status':("Inactivo", "Activo")[int.from_bytes(datos[7],byteorder='big')]}
                    return user
                elif datos[4] == email or datos[5] == user_name:
                    user={'Email':datos[4], 'Usuario':datos[5]}
                    return user
            else:
                return "Usuario encontrado con estatus inactivo."
        else:
            return None
        
    except Exception as ex:
        raise ex
    

#@cross_origin #Opción uno habilitar CORS de ruta en ruta
@app.route('/users', methods=['GET'])
def listar_usuarios():
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT * FROM usuario"

        cursor.execute(sql)
        datos =cursor.fetchall()

        users=[]

        print(datos)

        for fila in datos:
            # print(("Inactivo", "Activo")[int.from_bytes(fila[7],byteorder='big')])
            
            if ("Inactivo", "Activo")[int.from_bytes(fila[7],byteorder='big')] == "Activo":
                user={'Id':fila[0],'Nombre':fila[3],'Ape Pat':fila[1],'Ape Mat':fila[2],'Email':fila[4],'Usuario':fila[5],'Password':fila[6],'Status':("Inactivo", "Activo")[int.from_bytes(fila[7],byteorder='big')]}
                users.append(user)

        return jsonify({'users':users, 'mensaje':"Usuarios listados", 'exito':True})
    
    except Exception as ex:
        return jsonify({'mensaje':"Error", 'exito':False})
    

    
@app.route('/users/<id>', methods=['GET'])
def leer_usuario(id):
    try:
        # cursor=conexion.connection.cursor()
        # sql="SELECT * FROM usuario WHERE ID = '{0}'".format(id)

        # cursor.execute(sql)
        # datos =cursor.fetchone()

        #print(datos)
        user = leer_usuario_bd(id)
        if user == None:
            return jsonify({'mensaje':"Usuario no encontrado.", 'exito':False})
        elif user == "Usuario encontrado con estatus inactivo.":
            return jsonify({'mensaje':user, 'exito':False})
        else:
            # user={'Id':datos[0],'Nombre':datos[3],'Paterno':datos[1],'Materno':datos[2],'Email':datos[4],'Usuario':datos[5],'Password':datos[6]}
            return jsonify({'user':user, 'mensaje':"Usuario encontrado", 'exito':True})
    
    except Exception as ex:
        return jsonify({'mensaje':"Error"})
    

@app.route('/users', methods=['POST'])
def registrar_usuario():
    try:
        user = leer_usuario_bd(0, request.json['EMAIL'], request.json['USER_NAME'])
        
        if user == "Usuario encontrado con estatus inactivo.":
           return jsonify({'mensaje':"Existe un usario en estatus inactivo con email o usuario especificados.", 'exito':False})
        elif user == None:           
            cursor=conexion.connection.cursor()
            sql="""INSERT INTO USUARIO (PATERNO, MATERNO, NOMBRE, EMAIL, USER_NAME, PASSWORD) 
            VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')""".format(request.json['PATERNO'],
            request.json['MATERNO'],
            request.json['NOMBRE'],
            request.json['EMAIL'],
            request.json['USER_NAME'],
            request.json['PASSWORD'])

            cursor.execute(sql)
            conexion.connection.commit( )

            return jsonify({'mensaje':"Usuario registrado con éxito.", 'exito':True})
        elif user['Email'] == request.json['EMAIL'] or user['Usuario'] == request.json['USER_NAME']:
            return jsonify({'mensaje':"Ya existe un registro con el email o usuario especificado. (Usuario: "+user['Usuario']+", Email: " + user['Email']+")", 'exito':False})    

    
    except Exception as ex:
        return jsonify({'mensaje':"Error", 'exito':False})
    

@app.route('/users/<id>', methods=['PUT'])
def actualizar_usuario(id):
    try:
        user = leer_usuario_bd_by_id(id)
        
        if user != None:
            cursor=conexion.connection.cursor()
            sql="""UPDATE usuario SET  PATERNO = '{0}', MATERNO = '{1}',  NOMBRE = '{2}',  EMAIL = '{3}',  USER_NAME = '{4}',  PASSWORD = '{5}'
            WHERE ID = {6}""".format(request.json['PATERNO'],
            request.json['MATERNO'],
            request.json['NOMBRE'],
            request.json['EMAIL'],
            request.json['USER_NAME'],
            request.json['PASSWORD'],
            id)

            cursor.execute(sql)
            conexion.connection.commit( )

            return jsonify({'mensaje':"Usuario actualizado", 'exito':True})
        else:
            return jsonify({'mensaje':"Usuario no encontrado", 'exito':False})
    
    except Exception as ex:
        return jsonify({'mensaje':"Error", 'exito':False})
    
    
@app.route('/updateStatus/<id>', methods=['PUT'])
def actualizar_estatus_usuario(id):
    try:
        user = leer_usuario_bd_by_id(id)
        
        if user != None:
            cursor=conexion.connection.cursor()
            sql="UPDATE usuario SET STATUS = {0} WHERE ID = '{1}'".format(request.json['STATUS'],id)

            cursor.execute(sql)
            conexion.connection.commit( )
            return jsonify({'mensaje':"Estatus de usuario actualizado con éxito.", 'exito':True})
        else:
            return jsonify({'mensaje':"Usuario no encontrado", 'exito':False})
    
    except Exception as ex:
        return jsonify({'mensaje':"Error"})


@app.route('/users/<id>', methods=['DELETE'])
def eliminar_usuario(id):
    try:
        cursor=conexion.connection.cursor()
        sql="DELETE FROM usuario WHERE ID = '{0}'".format(id)

        cursor.execute(sql)
        conexion.connection.commit( )
        return jsonify({'mensaje':"Usuario eliminado"})
    
    except Exception as ex:
        return jsonify({'mensaje':"Error"})
    


    
def pagina_no_necontrada(error):
    return "<h1>La página que intentas buscar, no existe....</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_necontrada)
    app.run()
