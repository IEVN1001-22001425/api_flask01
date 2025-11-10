from flask import Flask, render_template, request
from flask import make_response, jsonify, flash
import json
import math
import forms
from datetime import datetime



app = Flask(__name__)

@app.route('/pizzas', methods=['POST', 'GET'])
def pizzas():
    form = forms.PizzaForm(request.form)
    pedidos = []
    ventas_dia = []
    total_dia = 0

    
    nombre_cliente_actual = request.cookies.get("cliente_nombre") or "Cliente sin nombre"
    direccion_cliente_actual = request.cookies.get("cliente_direccion")
    telefono_cliente_actual = request.cookies.get("cliente_telefono")

    data_pedidos = request.cookies.get("pedidos")
    data_ventas = request.cookies.get("ventas")

    if data_pedidos:
        pedidos = json.loads(data_pedidos)
    if data_ventas:
        ventas_dia = json.loads(data_ventas)

    total_dia = sum(v['total'] for v in ventas_dia)

   
    if request.method == 'POST':
        accion = request.form.get("accion")

        
        if accion == "quitar":
            if pedidos:
                pedidos.pop()

        
        elif accion == "terminar":
            total = sum(p['subtotal'] for p in pedidos)
            cliente = nombre_cliente_actual
            direccion = direccion_cliente_actual
            telefono = telefono_cliente_actual
            fecha_venta = datetime.now().strftime("%d-%m-%Y")

            if pedidos:
                ventas_dia.append({
                    "nombre": cliente,
                    "direccion": direccion,
                    "telefono": telefono,
                    "fecha": fecha_venta,
                    "total": total
                })
                pedidos = []

            
            nombre_cliente_actual = "Cliente sin nombre"
            direccion_cliente_actual = None
            telefono_cliente_actual = None

       
        elif accion == "totales":
            total_dia = sum(v['total'] for v in ventas_dia)

        
        elif accion == "agregar" and form.validate():
            
            nombre_cliente_actual = form.nombre.data
            direccion_cliente_actual = form.direccion.data
            telefono_cliente_actual = form.telefono.data

            tamano = form.tamano.data
            ingredientes = form.ingredientes.data
            num_pizzas = form.num_pizzas.data

            precios_tamano = {'chica': 40, 'mediana': 80, 'grande': 120}
            precio = precios_tamano[tamano]
            precio += len(ingredientes) * 10
            subtotal = precio * num_pizzas

            pedido = {
                "tamano": tamano,
                "ingredientes": ", ".join(ingredientes) if ingredientes else "Ninguno",
                "num_pizzas": num_pizzas,
                "subtotal": subtotal
            }
            pedidos.append(pedido)

    
    response = make_response(render_template(
        "pizzas.html",
        form=form,
        pedidos=pedidos,
        ventas_dia=ventas_dia,
        total_dia=total_dia
    ))

    
    response.set_cookie("pedidos", json.dumps(pedidos))
    response.set_cookie("ventas", json.dumps(ventas_dia))

    
    if nombre_cliente_actual == "Cliente sin nombre":
        response.delete_cookie("cliente_nombre")
        response.delete_cookie("cliente_direccion")
        response.delete_cookie("cliente_telefono")
    else:
        response.set_cookie("cliente_nombre", nombre_cliente_actual)
        response.set_cookie("cliente_direccion", direccion_cliente_actual or "")
        response.set_cookie("cliente_telefono", telefono_cliente_actual or "")

    return response




@app.route("/ver_cookies_pizzas")
def ver_cookies_pizzas():
    
    datos_cookies = {}
    
    
    data_pedidos = request.cookies.get("pedidos")
    if data_pedidos:
        try:
            datos_cookies['pedidos'] = json.loads(data_pedidos)
        except json.JSONDecodeError:
            datos_cookies['pedidos'] = "Error al decodificar la cookie de pedidos"
    else:
        datos_cookies['pedidos'] = "No hay pedidos pendientes guardados."
        
    
    data_ventas = request.cookies.get("ventas")
    if data_ventas:
        try:
            datos_cookies['ventas_dia'] = json.loads(data_ventas)
        except json.JSONDecodeError:
            datos_cookies['ventas_dia'] = "Error al decodificar la cookie de ventas"
    else:
        datos_cookies['ventas_dia'] = "No hay registro de ventas guardadas."
        

    if not data_pedidos and not data_ventas:
        return jsonify({"mensaje": "No se encontraron cookies de pedidos ni de ventas."}), 404

    return jsonify(datos_cookies)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/index')
def index():
    titulo = "IEVN1001"
    listado = ["Python", "Flask", "HTML", "CSS", "JavaScript"]
    return render_template('index.html', titulo=titulo, listado=listado)

@app.route('/aporb')
def aporb():
    return render_template('aporb.html')

@app.route('/resultado', methods=['POST']) #INDICAR EL METODO
def resultado():
    n1 = request.form.get("a") #poner el valor del name del input
    n2 = request.form.get("b")
    return "La multiplicación de {} y {} es {}".format(n1,n2,int(n1)*int(n2))


@app.route('/distancia', methods=['POST', 'GET'])
def distancia(): 
    resultado = None 
   
    if request.method == 'POST':
       
        
       
        x1 = float(request.form['x1'])
        y1 = float(request.form['y1'])
        x2 = float(request.form['x2'])
        y2 = float(request.form['y2'])

       
        dx = x2 - x1
        dy = y2 - y1
        
        
        distancia_puntos = math.sqrt(dx**2 + dy**2)
        
        
        resultado = round(distancia_puntos, 2)
            
   
    return render_template('distancia.html', distancia=resultado)

    
@app.route("/figuras", methods=['POST', 'GET'])
def figuras():

    resultado_area = None

    if request.method == 'POST':
        figura = request.form.get('figura')
        
        
        base = float(request.form.get('base') or 0)
        altura = float(request.form.get('altura') or 0)
        radio = float(request.form.get('radio') or 0)
        apotema = float(request.form.get('apotema') or 0)

        
        if figura == 'rectangulo':
            if base > 0 and altura > 0:
                resultado_area = base * altura
                
        elif figura == 'triangulo':
            if base > 0 and altura > 0:
                resultado_area = (base * altura) / 2

        elif figura == 'circulo':
            if radio > 0:
                resultado_area = math.pi * (radio ** 2)
        elif figura == 'pentagono':
            if base > 0 and apotema > 0:
               perimetro = 5 * base   
               resultado_area = (perimetro * apotema) / 2
        

        
            
        resultado_final = f"El área de {figura} es: {resultado_area}"
        return render_template('figuras.html', resultado_area=resultado_final)
        
    
    return render_template('figuras.html')
    

@app.route("/hola") #crear rutas
def func():    #funcion siempre devuelve algo (return)
    return "<h1>Hola</h1>"

@app.route("/alumnos",methods=['POST', 'GET']) #crear rutas
def alumnos():
    mat=0
    nom=''
    apell=''
    email=''
    estudiantes=[]
    datos={}

    alumno_clas=forms.UserForm(request.form)
    if request.method=='POST' and alumno_clas.validate():

        if request.form.get("btnEliminar")=='eliminar': #eliminar cookie
            response = make_response(render_template('Alumnos.html',))
            response.delete_cookie('usuario')

        mat=alumno_clas.matricula.data
        nom=alumno_clas.nombre.data
        apell=alumno_clas.apellido.data
        email=alumno_clas.email.data

        datos={'matricula': mat, #almacenar en diccionario
               'nombre': nom.rstrip(),#quitar espacios
               'apellido':apell.rstrip(),
               'email':email.strip()
               }
        
        data_str = request.cookies.get("usuario") #crear cookie
        if not data_str: #si no hay cookie manda:
            return "No hay cookie guardada", 404
        
        estudiantes = json.loads(data_str) #cargar al arreglo
        estudiantes.append(datos) #añadir registro al diccionario

        #response para regresar cookies
    response = make_response(render_template('Alumnos.html', form=alumno_clas, mat=mat, nom=nom, apell=apell, email=email))
    
    if request.method!='GET': #diferente de GET
        response.set_cookie('usuario', json.dumps(estudiantes))

    return response #carga la cookie (ruta termina aqui)

@app.route("/get_cookie")
def get_cookies():
    data_str = request.cookies.get("usuario")
    if not data_str:
        return "No hay cookie guardada", 404
    estudiantes =json.loads(data_str)

    return jsonify(estudiantes)

   

@app.route("/distanciapuntos",methods=['POST', 'GET']) #crear rutas
def distancia2():
    x1=0
    y1=0
    x2=0
    y2=0
    resultado=0
    punto_clas=forms.UserForm(request.form)
    if request.method=='POST' and punto_clas.validate():
        x1punto=punto_clas.x1.data
        y1punto=punto_clas.y1.data
        x2punto=punto_clas.x2.data
        y2punto=punto_clas.y2.data

        dx = x2punto - x1punto
        dy = y2punto - y1punto
        
        
        distancia_puntos = math.sqrt(dx**2 + dy**2)
        
        
        resultado = round(distancia_puntos, 2)


    return render_template('distanciapuntos.html', form=punto_clas, resultado=resultado)



@app.route("/user/<string:user>")  #pasar parametro 
def user(user):    #nombre de la variable del parametro
    return "<h1>Hola, {}</h1>".format(user) #format = para imprimir en pantalla

@app.route("/square/<int:num>") 
def square(num):    
    return "<h1>The square of {} is {}.</h1>".format(num, num**2)

@app.route("/repeat/<string:text>/<int:times>") 
def repeat(text, times):    
    return "<h1>" + "".join([text] * times) + "</h1>" #join unir

@app.route("/suma/<float:a>/ <float:b>") 
def suma(a, b):    
    return "<h1>The sum of {} and {} is {}.</h1>".format(a, b,  a + b)




if __name__ == '__main__':
    app.run(debug=True)

