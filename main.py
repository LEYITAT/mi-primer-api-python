
from flask import Flask, jsonify


app = Flask(__name__)

@app.route('/')
def hello_world_endpoint():
    """
      http://127.0.0.1:5000/
    """
    return "Hello world!"

@app.route('/datos_json')
def obtener_datos_json():
    """
     http://127.0.0.1:5000/datos_json
    """
    datos = {
        "Situacion": "No se que estoy haciendo xd",
        "Sentimiento": "Acabada y media, frustrada, lo que sigue",
        "Podre con esto?": "Espero que si",
        "YO Puedo con todo?": "Claro que yes",
        "Update": "Sigo sin saber que estoy haciendo xD",
        
    }
    return jsonify(datos) 

if __name__ == '__main__':

    app.run(debug=True)