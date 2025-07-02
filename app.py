from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

@app.route('/hello_text')
def hello_world_endpoint():

 """http://127.0.0.1:5000/hello_text
"""
 return "Hello world"

@app.route('/datos_json', methods=['GET', 'POST'])
def obtener_datos_json():
    """
     http://127.0.0.1:5000/datos_json
    """
    if request.method == 'POST':
        try:
            data_from_post = request.get_json(force=True, silent=True)
            if data_from_post is None:
                
                return render_template('400.html'), 400
            
            datos_respuesta = {
                "Mensaje": "Datos POST recibidos correctamente",
                "Datos_Recibidos": data_from_post,
                "Fecha_Actual": "Fecha y hora no disponibles (sin modulo datetime)"
            }
            return jsonify(datos_respuesta)
        except Exception as e:
            
            return render_template('400.html'), 400
    else:
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

@app.errorhandler(400)
def bad_request_error(error):
    return render_template('400.html'), 400

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(405)
def method_not_allowed_error(error):
    return render_template('405.html'), 405

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)