from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from math import sqrt

app = Flask(__name__)

# Función para calcular el discriminante
def discriminante(a, b, c):
    d = b**2 - 4 * a * c
    if d > 0:
        x1 = (-b + sqrt(d)) / (2 * a)
        x2 = (-b - sqrt(d)) / (2 * a)
        resultado = f"Tiene dos soluciones reales: x1 = {x1:.2f}, x2 = {x2:.2f}"
    elif d == 0:
        x1 = -b / (2 * a)
        resultado = f"Tiene una única solución real: x1 = x2 = {x1:.2f}"
    else:
        resultado = "No tiene soluciones reales."
    return resultado

# Función para calcular y graficar la función cuadrática
def generar_grafico(a, b, c):
    x = np.linspace(-10, 10, 400)
    y = a * x**2 + b * x + c

    fig, ax = plt.subplots()
    ax.plot(x, y, label=f'$y = {a}x^2 + {b}x + {c}$', color='b')
    ax.set_title('Gráfico de la Ecuación Cuadrática')
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.grid(True)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.legend()

    # Convertir la gráfica a imagen 
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close(fig)

    return plot_url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Obtener valores del formulario
            a = float(request.form['a'])
            b = float(request.form['b'])
            c = float(request.form['c'])

            # Calcular el discriminante
            resultado = discriminante(a, b, c)

            # Generar el gráfico
            grafico = generar_grafico(a, b, c)

            return render_template('index.html', resultado=resultado, grafico=grafico)
        except ValueError:
            return render_template('index.html', error="Por favor, introduce valores numéricos válidos.")
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

#hello