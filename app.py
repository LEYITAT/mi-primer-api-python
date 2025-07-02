from flask import Flask, jsonify, render_template, request
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/hello_text')
def hello_world_endpoint():
    """
    Este endpoint saluda al mundo.
    ---
    responses:
      200:
        description: Un mensaje de saludo.
        schema:
          type: string
          example: "Hello world"
    """
    return "Hello world"

@app.route('/datos_json', methods=['GET', 'POST'])
def obtener_datos_json():
    """
    Obtiene o procesa datos en formato JSON.
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            mensaje:
              type: string
              description: Un mensaje de ejemplo.
              example: "Hola desde POST"
        description: Datos JSON para enviar (solo para POST).
        required: false
    responses:
      200:
        description: Datos JSON devueltos o confirmación de POST.
        schema:
          type: object
          properties:
            Situacion:
              type: string
            Sentimiento:
              type: string
            Podre con esto?:
              type: string
            YO Puedo con todo?:
              type: string
            Update:
              type: string
            Fecha_Actual:
              type: string
          example:
            Situacion: "no se que ando haciendo nuevamente"
            Sentimiento: "tuve que hacerlo todo de cero xD por que tenia que integrar el html"
            Podre con esto?: "of course siempre mami"
            YO Puedo con todo?": "Claro que yes solo dios puede juzgarme"
            Update: "Tratando de ver la luz al final del tunel"
            Fecha_Actual: "Fecha y hora no disponibles (sin modulo datetime)"
      400:
        description: Solicitud incorrecta debido a JSON mal formado.
        schema:
          type: string
          example: "Error: JSON mal formado o Content-Type incorrecto"
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
    Página principal que muestra información sobre criaturas fantásticas.
    ---
    responses:
      200:
        description: Página HTML de animales fantásticos.
        schema:
          type: string
          example: "<html>...</html>"
    """
    current_time = "Hora no disponible (sin modulo datetime)"
    return render_template('animalesfantasticos.html', current_time=current_time)

@app.errorhandler(400)
def bad_request_error(error):
    """
    Maneja errores 400 Bad Request.
    ---
    responses:
      400:
        description: Página de error 400.
        schema:
          type: string
          example: "<html>...</html>"
    """
    return render_template('400.html'), 400

@app.errorhandler(404)
def not_found_error(error):
    """
    Maneja errores 404 Not Found.
    ---
    responses:
      404:
        description: Página de error 404.
        schema:
          type: string
          example: "<html>...</html>"
    """
    return render_template('404.html'), 404

@app.errorhandler(405)
def method_not_allowed_error(error):
    """
    Maneja errores 405 Method Not Allowed.
    ---
    responses:
      405:
        description: Página de error 405.
        schema:
          type: string
          example: "<html>...</html>"
    """
    return render_template('405.html'), 405

@app.errorhandler(500)
def internal_error(error):
    """
    Maneja errores 500 Internal Server Error.
    ---
    responses:
      500:
        description: Página de error 500.
        schema:
          type: string
          example: "<html>...</html>"
    """
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)