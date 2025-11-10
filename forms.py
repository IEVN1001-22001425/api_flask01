from wtforms import EmailField,Form
from wtforms import StringField,IntegerField,BooleanField,PasswordField,FloatField,RadioField,SelectMultipleField,widgets
from wtforms.widgets import CheckboxInput
from wtforms import validators


"""class UserForm(Form): distancia puntos
    x1 = FloatField('Punto x1',[validators.DataRequired(message='Ingrese un numero')])
    y1 = FloatField('Punto y1', [validators.DataRequired(message='Ingrese un numero')])
    x2 = FloatField('Punto x2', [validators.DataRequired(message='El campo es requerido')])
    y2 = FloatField('Punto y2', [validators.DataRequired(message='Ingrese un numero')])"""

"""class UserForm(Form): #alumnos
    matricula = IntegerField('Matricula', [validators.DataRequired(message='El campo es requerido')])
    nombre = StringField('Nombre', [validators.DataRequired(message='El campo es requerido'), validators.Length(min=1, max=50)])
    apellido = StringField('Apellido', [validators.DataRequired(message='El campo es requerido'), validators.Length(min=1, max=50)])
    email = EmailField('Correo', [validators.DataRequired(message='El campo es requerido')])"""



class PizzaForm(Form):
    """
    Formulario para la toma de pedidos de pizza.
    """
    nombre = StringField('Nombre', [
        validators.DataRequired(message="Ingrese el nombre del cliente")
    ])
    
    direccion = StringField('Dirección', [
        validators.DataRequired(message="Ingrese la dirección")
    ])
    
    telefono = StringField('Teléfono', [
        validators.DataRequired(message="Ingrese el teléfono")
    ])
    
    tamano = RadioField('Tamaño de Pizza', choices=[
        ('chica', 'Chica $40'),
        ('mediana', 'Mediana $80'),
        ('grande', 'Grande $120')
    ], validators=[
        validators.DataRequired(message="Seleccione un tamaño")
    ])
    
    ingredientes = SelectMultipleField('Ingredientes', choices=[
        ('jamon', 'Jamón $10'),
        ('pina', 'Piña $10'),
        ('champi', 'Champiñones $10')
    ], option_widget=widgets.CheckboxInput(), 
       widget=widgets.ListWidget(prefix_label=False)
    )
    
    num_pizzas = IntegerField('Número de Pizzas', [
        validators.DataRequired(message="Ingrese el número de pizzas"),
        validators.NumberRange(min=1, message="El número debe ser al menos 1") # Opcional: valida que sea un número positivo
    ])