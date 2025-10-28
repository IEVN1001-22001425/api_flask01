from flask import Flask, render_template, request
import math


app = Flask(__name__)

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
