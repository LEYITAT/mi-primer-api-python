from flask import Flask, jsonify, render_template


app = Flask(__name__)


@app.route('/hello_text')
def hello_world_endpoint():
    """

 http://127.0.0.1:5000/hello_text

    """
    return "Hello world"


@app.route('/datos_json')
def obtener_datos_json():
    """
     http://127.0.0.1:5000/datos_json
    """
    datos = {
        "Situacion": "no se que ando haciendo nuevamente",
        "Sentimiento": "tuve que hacerlo todo de cero xD por que tenia que integrar el html",
        "Podre con esto?": "of course siempre mami",
        "YO Puedo con todo?": "Claro que yes solo dios puede juzgarme",
        "Update": "Tratando de ver la luz al final del tunel",
        "Fecha_Actual": "Fecha y hora no disponibles (sin modulo datetime)" 
    }
    return jsonify(datos)


@app.route('/')
def animales_fantasticos_html():
    """
    http://127.0.0.1:5000/
    """
    current_time = "Hora no disponible (sin modulo datetime)" 

    return render_template('animalesfantasticos.html', current_time=current_time)




@app.errorhandler(404)
def not_found_error(error):
    """
   '404.html'
    """
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """
    '500.html'.
    """
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)

