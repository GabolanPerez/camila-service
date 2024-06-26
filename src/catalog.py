from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app) #Opción uno habilitar CORS de ruta en ruta

conexion=MySQL(app)

CORS(app, origins="*") #Con esot habilitamos todas las rutas dando permiso a los CORS

# CORS(app, resources={r"/users/*": {"origins": "htpp://localhost"}}) #Habilitando CORS por dominio}

def leer_talla_by_id(id):
    try:
        cursor = conexion.connection.cursor()
        sql="SELECT * FROM talla WHERE ID = '{0}'".format(id)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            talla={'Id':datos[0],'Descripcion':datos[1]}
            return talla
        else:
            return None
    except Exception as ex:
        raise ex
    

@app.route('/tallas', methods=['GET'])
def listar_talla():
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT * FROM talla"

        cursor.execute(sql)
        datos =cursor.fetchall()

        tallas=[]

        print(datos)

        for fila in datos:
            
            talla={'Id':fila[0],'Descricion':fila[1]}
            tallas.append(talla)

        return jsonify({'tallas':tallas, 'mensaje':"Tallas listadas", 'exito':True})
    
    except Exception as ex:
        return jsonify({'mensaje':"Error", 'exito':False})
    
    


@app.route('/tallas/<id>', methods=['GET'])
def leer_talla(id):
    try:
        talla = leer_talla_by_id(id)
        return jsonify({'talla':talla, 'mensaje':"Talla encontrada", 'exito':True})
    
    except Exception as ex:
        return jsonify({'mensaje':"Error"})



@app.route('/tallas', methods=['POST'])
def registrar_talla():
    try:      
        cursor=conexion.connection.cursor()
        sql="""INSERT INTO TALLA (DESCRIPCION) 
        VALUES ('{0}')""".format(request.json['DESCRIPCION'])

        cursor.execute(sql)
        conexion.connection.commit( )

        return jsonify({'mensaje':"Talla registrada con éxito.", 'exito':True})
    
    except Exception as ex:
        return jsonify({'mensaje':"Error", 'exito':False})
    
    
@app.route('/tallas/<id>', methods=['PUT'])
def actualizar_talla(id):
    try:
            cursor=conexion.connection.cursor()
            sql="""UPDATE talla SET  DESCRIPCION = '{0}' WHERE ID = {1}""".format(request.json['DESCRIPCION'],id)

            cursor.execute(sql)
            conexion.connection.commit( )

            return jsonify({'mensaje':"Talla actualizada", 'exito':True})
    
    except Exception as ex:
        return jsonify({'mensaje':"Error", 'exito':False})
    







def leer_color_by_id(id):
    try:
        cursor = conexion.connection.cursor()
        sql="SELECT * FROM color WHERE ID = '{0}'".format(id)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            color={'Id':datos[0],'Descripcion':datos[1]}
            return color
        else:
            return None
    except Exception as ex:
        raise ex
    

@app.route('/colores', methods=['GET'])
def listar_color():
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT * FROM color"

        cursor.execute(sql)
        datos =cursor.fetchall()

        colores=[]

        for fila in datos:
            
            color={'Id':fila[0],'Descricion':fila[1]}
            colores.append(color)

        return jsonify({'colores':colores, 'mensaje':"Colores listados", 'exito':True})
    
    except Exception as ex:
        return jsonify({'mensaje':"Error", 'exito':False})
    
    


@app.route('/colores/<id>', methods=['GET'])
def leer_color(id):
    try:
        color = leer_color_by_id(id)
        return jsonify({'color':color, 'mensaje':"Color encontrado", 'exito':True})
    
    except Exception as ex:
        return jsonify({'mensaje':"Error"})



@app.route('/colores', methods=['POST'])
def registrar_color():
    try:      
        cursor=conexion.connection.cursor()
        sql="""INSERT INTO color (DESCRIPCION) 
        VALUES ('{0}')""".format(request.json['DESCRIPCION'])

        cursor.execute(sql)
        conexion.connection.commit( )

        return jsonify({'mensaje':"Color registrado con éxito.", 'exito':True})
    
    except Exception as ex:
        return jsonify({'mensaje':"Error", 'exito':False})
    
    
@app.route('/colores/<id>', methods=['PUT'])
def actualizar_color(id):
    try:
            cursor=conexion.connection.cursor()
            sql="""UPDATE color SET  DESCRIPCION = '{0}' WHERE ID = {1}""".format(request.json['DESCRIPCION'],id)

            cursor.execute(sql)
            conexion.connection.commit( )

            return jsonify({'mensaje':"Color actualizado", 'exito':True})
    
    except Exception as ex:
        return jsonify({'mensaje':"Error", 'exito':False})
    







def leer_modelo_by_id(id):
    try:
        cursor = conexion.connection.cursor()
        sql="SELECT * FROM modelo WHERE ID = '{0}'".format(id)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            modelo={'Id':datos[0],'Descripcion':datos[1]}
            return modelo
        else:
            return None
    except Exception as ex:
        raise ex
    

@app.route('/modelos', methods=['GET'])
def listar_modelo():
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT * FROM modelo"

        cursor.execute(sql)
        datos =cursor.fetchall()

        modelos=[]

        for fila in datos:
            
            modelo={'Id':fila[0],'Descricion':fila[1]}
            modelos.append(modelo)

        return jsonify({'modelos':modelos, 'mensaje':"Modelos listados", 'exito':True})
    
    except Exception as ex:
        return jsonify({'mensaje':"Error", 'exito':False})
    
    


@app.route('/modelos/<id>', methods=['GET'])
def leer_modelo(id):
    try:
        modelo = leer_modelo_by_id(id)
        return jsonify({'modelo':modelo, 'mensaje':"Modelo encontrado", 'exito':True})
    
    except Exception as ex:
        return jsonify({'mensaje':"Error"})



@app.route('/modelos', methods=['POST'])
def registrar_modelo():
    try:      
        cursor=conexion.connection.cursor()
        sql="""INSERT INTO modelo (DESCRIPCION) 
        VALUES ('{0}')""".format(request.json['DESCRIPCION'])

        cursor.execute(sql)
        conexion.connection.commit( )

        return jsonify({'mensaje':"Modelo registrado con éxito.", 'exito':True})
    
    except Exception as ex:
        return jsonify({'mensaje':"Error", 'exito':False})
    
    
@app.route('/modelos/<id>', methods=['PUT'])
def actualizar_modelo(id):
    try:
            cursor=conexion.connection.cursor()
            sql="""UPDATE modelo SET  DESCRIPCION = '{0}' WHERE ID = {1}""".format(request.json['DESCRIPCION'],id)

            cursor.execute(sql)
            conexion.connection.commit( )

            return jsonify({'mensaje':"Modelo actualizado", 'exito':True})
    
    except Exception as ex:
        return jsonify({'mensaje':"Error", 'exito':False})






def leer_genero_by_id(id):
    try:
        cursor = conexion.connection.cursor()
        sql="SELECT * FROM genero WHERE ID = '{0}'".format(id)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            genero={'Id':datos[0],'Descripcion':datos[1]}
            return genero
        else:
            return None
    except Exception as ex:
        raise ex
    

@app.route('/generos', methods=['GET'])
def listar_genero():
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT * FROM genero"

        cursor.execute(sql)
        datos =cursor.fetchall()

        generos=[]

        for fila in datos:
            
            genero={'Id':fila[0],'Descricion':fila[1]}
            generos.append(genero)

        return jsonify({'generos':generos, 'mensaje':"Generos listados", 'exito':True})
    
    except Exception as ex:
        return jsonify({'mensaje':"Error", 'exito':False})
    
    


@app.route('/generos/<id>', methods=['GET'])
def leer_genero(id):
    try:
        genero = leer_genero_by_id(id)
        return jsonify({'genero':genero, 'mensaje':"Genero encontrado", 'exito':True})
    
    except Exception as ex:
        return jsonify({'mensaje':"Error"})



@app.route('/generos', methods=['POST'])
def registrar_genero():
    try:      
        cursor=conexion.connection.cursor()
        sql="""INSERT INTO genero (DESCRIPCION) 
        VALUES ('{0}')""".format(request.json['DESCRIPCION'])

        cursor.execute(sql)
        conexion.connection.commit( )

        return jsonify({'mensaje':"Color registrado con éxito.", 'exito':True})
    
    except Exception as ex:
        return jsonify({'mensaje':"Error", 'exito':False})
    
    
@app.route('/generos/<id>', methods=['PUT'])
def actualizar_genero(id):
    try:
            cursor=conexion.connection.cursor()
            sql="""UPDATE genero SET  DESCRIPCION = '{0}' WHERE ID = {1}""".format(request.json['DESCRIPCION'],id)

            cursor.execute(sql)
            conexion.connection.commit( )

            return jsonify({'mensaje':"Genero actualizado", 'exito':True})
    
    except Exception as ex:
        return jsonify({'mensaje':"Error", 'exito':False})
    







def pagina_no_necontrada(error):
    return "<h1>La página que intentas buscar, no existe....</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_necontrada)
    app.run()