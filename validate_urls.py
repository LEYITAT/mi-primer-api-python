import requests
import time
import os

BASE_URL = "http://127.0.0.1:5000"

def test_endpoint(url, expected_status=200, method='GET', json_data=None, raw_data=None, headers=None):
    print(f"\n--- Probando: {method} {url} ---")
    try:
        response = None
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            if json_data is not None:
                response = requests.post(url, json=json_data, headers=headers)
            elif raw_data is not None:
                response = requests.post(url, data=raw_data, headers=headers)
            else:
                response = requests.post(url, headers=headers)
        elif method == 'PUT':
            if json_data is not None:
                response = requests.put(url, json=json_data, headers=headers)
            elif raw_data is not None:
                response = requests.put(url, data=raw_data, headers=headers)
            else:
                response = requests.put(url, headers=headers)
        elif method == 'DELETE':
            response = requests.delete(url)
        else:
            print(f"Método HTTP '{method}' no soportado por el script de prueba.")
            return False

        if response is None:
            print("❌ Fallo: No se generó respuesta para el método HTTP.")
            return False

        print(f"Estado HTTP: {response.status_code}")
        print(f"Contenido (primeras 200 caracteres): {response.text[:200]}...")

        if response.status_code == expected_status:
            print(f"✅ Éxito: El endpoint respondió con el estado {expected_status} esperado.")
            return True
        else:
            print(f"❌ Fallo: Se esperaba el estado {expected_status}, pero se obtuvo {response.status_code}.")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Fallo: No se pudo conectar al servidor Flask. Asegúrate de que esté corriendo.")
        return False
    except Exception as e:
        print(f"❌ Fallo: Ocurrió un error inesperado: {e}")
        return False

def main():
    print("Iniciando pruebas de validación de URLs de Flask...")
    print("Asegúrarse de que tu aplicación 'app.py' esté corriendo en http://127.0.0.1:5000/\n")

    time.sleep(2)

    all_tests_passed = True

    print("\n--- Probando Endpoints Definidos ---")
    if not test_endpoint(f"{BASE_URL}/hello_text"):
        all_tests_passed = False

    if not test_endpoint(f"{BASE_URL}/datos_json"):
        all_tests_passed = False
    else:
        try:
            json_data = requests.get(f"{BASE_URL}/datos_json").json()
            if "Situacion" in json_data and "Fecha_Actual" in json_data:
                print("✅ Éxito: El JSON contiene las claves esperadas.")
            else:
                print("❌ Fallo: El JSON no contiene las claves esperadas.")
                all_tests_passed = False
        except Exception as e:
            print(f"❌ Fallo: No se pudo parsear el JSON o verificar claves: {e}")
            all_tests_passed = False

    if not test_endpoint(f"{BASE_URL}/"):
        all_tests_passed = False
    else:
        response_text = requests.get(f"{BASE_URL}/").text
        if "Criaturas Fantásticas de Nuestro Mundo" in response_text:
            print("✅ Éxito: El HTML de la ruta raíz contiene el título esperado.")
        else:
            print("❌ Fallo: El HTML de la ruta raíz no contiene el título esperado.")
            all_tests_passed = False

    print("\n--- Probando Manejadores de Errores ---")

    if not test_endpoint(f"{BASE_URL}/ruta_inexistente", expected_status=404):
        all_tests_passed = False
    else:
        response_text = requests.get(f"{BASE_URL}/ruta_inexistente").text
        if "Error 404" in response_text:
            print("✅ Éxito: La página 404 contiene el texto esperado.")
        else:
            print("❌ Fallo: La página 404 no contiene el texto esperado.")
            all_tests_passed = False

    if not test_endpoint(f"{BASE_URL}/hello_text", expected_status=405, method='POST'):
        all_tests_passed = False
    else:
        response_text = requests.post(f"{BASE_URL}/hello_text").text
        if "Error 405" in response_text:
            print("✅ Éxito: La página 405 contiene el texto esperado.")
        else:
            print("❌ Fallo: La página 405 no contiene el texto esperado.")
            all_tests_passed = False

    print("\n--- Probando Error 500 (simulando plantilla faltante) ---")
    template_path = os.path.join('templates', 'animalesfantasticos.html')
    temp_template_path = os.path.join('templates', 'temp_animalesfantasticos.html')

    if os.path.exists(template_path):
        os.rename(template_path, temp_template_path)
        print(f"Renombrado '{template_path}' a '{temp_template_path}' para simular error 500.")
        if not test_endpoint(f"{BASE_URL}/", expected_status=500):
            all_tests_passed = False
        else:
            response_text = requests.get(f"{BASE_URL}/").text
            if "jinja2.exceptions.TemplateNotFound" in response_text or "Werkzeug Debugger" in response_text:
                print("✅ Éxito: Se detectó la página de error 500 de depuración (Werkzeug).")
            else:
                print("❌ Fallo: La página 500 no contiene el texto esperado para el modo debug.")
                all_tests_passed = False
        os.rename(temp_template_path, template_path)
        print(f"Restaurado '{temp_template_path}' a '{template_path}'.")
    else:
        print(f"Advertencia: '{template_path}' no encontrado. No se pudo probar el error 500 por plantilla faltante.")
        print("Asegurar que 'animalesfantasticos.html' exista para esta prueba.")

    print("\n--- Probando Error 400 (simulación con JSON malformado) ---")
    if not test_endpoint(f"{BASE_URL}/datos_json", expected_status=400, method='POST', raw_data="esto no es json {", headers={'Content-Type': 'application/json'}):
        all_tests_passed = False
    else:
        response_text = requests.post(f"{BASE_URL}/datos_json", data="esto no es json {", headers={'Content-Type': 'application/json'}).text
        if "Error 400" in response_text:
            print("✅ Éxito: La página 400 contiene el texto esperado.")
        else:
            print("❌ Fallo: La página 400 no contiene el texto esperado.")
            all_tests_passed = False

    print("\n--- Resumen de Pruebas ---")
    if all_tests_passed:
        print("🎉 ¡Todas las pruebas básicas de URLs pasaron con éxito!")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa los mensajes anteriores.")

if __name__ == '__main__':
    main()