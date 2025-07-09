from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from aria import Aria
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

usuarios = {}

def obtener_ia(nombre_usuario):
    if nombre_usuario not in usuarios:
        usuarios[nombre_usuario] = Aria(nombre_usuario)
    return usuarios[nombre_usuario]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mensaje", methods=["POST"])
def mensaje():
    datos = request.get_json()
    entrada = datos.get("mensaje", "")
    idioma = datos.get("idioma", "es")
    usuario = datos.get("usuario", "anonimo")
    ia = obtener_ia(usuario)
    ia.set_language(idioma)
    respuesta = ia.procesar_entrada(entrada)
    return jsonify({"respuesta": respuesta})

@app.route("/reiniciar", methods=["POST"])
def reiniciar():
    datos = request.get_json()
    usuario = datos.get("usuario", "anonimo")
    ia = obtener_ia(usuario)
    ia.reiniciar()
    return jsonify({"respuesta": f"{usuario} ha sido reiniciado."})

@app.route("/archivo", methods=["POST"])
def archivo():
    usuario = request.form.get("usuario", "anonimo")
    ia = obtener_ia(usuario)
    if "archivo" not in request.files:
        return jsonify({"respuesta": "No se encontró el archivo."})
    archivo = request.files["archivo"]
    if archivo.filename == "":
        return jsonify({"respuesta": "Nombre de archivo vacío."})
    nombre_seguro = secure_filename(archivo.filename)
    ruta = os.path.join(app.config["UPLOAD_FOLDER"], nombre_seguro)
    archivo.save(ruta)
    respuesta = ia.procesar_archivo(ruta)
    return jsonify({"respuesta": respuesta})

@app.route("/estadisticas", methods=["POST"])
def estadisticas():
    datos = request.get_json()
    usuario = datos.get("usuario", "anonimo")
    ia = obtener_ia(usuario)
    respuesta = ia.mostrar_estadisticas()
    return jsonify({"respuesta": respuesta})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

@app.route("/consultar", methods=["POST"])
def consultar():
    datos = request.get_json()
    mensaje = datos.get("mensaje", "")
    usuario = datos.get("usuario", "anonimo")
    with open("consultas.txt", "a", encoding="utf-8") as f:
        f.write(f"[{usuario}] {mensaje}\n")
    return jsonify({"respuesta": "Consulta enviada al creador. Gracias."})
