import json
import os
import datetime
from utils import buscar_en_internet, traducir_texto, extraer_texto_archivo

class Aria:
    def __init__(self, nombre_usuario):
        self.nombre_usuario = nombre_usuario
        self.ruta_memoria = f"memorias/{nombre_usuario}.json"
        self.idioma = "es"
        self.dia = datetime.date.today().isoformat()
        self.memoria = self.cargar_memoria()
        self.historial = self.memoria.get("historial", [])
        self.personalidad = self.memoria.get("personalidad", "amigable")
        self.stats = self.memoria.get("stats", {"mensajes": 0, "busquedas": 0, "reinicios": 0})

    def cargar_memoria(self):
        if os.path.exists(self.ruta_memoria):
            with open(self.ruta_memoria, "r") as f:
                return json.load(f)
        else:
            return {
                "nombre": self.nombre_usuario,
                "personalidad": "amigable",
                "historial": [],
                "stats": {"mensajes": 0, "busquedas": 0, "reinicios": 0}
            }

    def guardar_memoria(self):
        self.memoria["historial"] = self.historial
        self.memoria["personalidad"] = self.personalidad
        self.memoria["stats"] = self.stats
        with open(self.ruta_memoria, "w") as f:
            json.dump(self.memoria, f, indent=4)

    def set_language(self, lang):
        self.idioma = lang

    def procesar_entrada(self, entrada):
        entrada_l = entrada.lower()
        self.stats["mensajes"] += 1

        if "buscar" in entrada_l:
            tema = entrada_l.split("buscar")[-1].strip()
            resultado = buscar_en_internet(tema, self.idioma)
            self.stats["busquedas"] += 1
        elif "personalidad" in entrada_l:
            tipo = entrada_l.split("personalidad")[-1].strip()
            self.personalidad = tipo
            resultado = f"Personalidad cambiada a: {tipo}"
        elif "historial" in entrada_l:
            resultado = self.mostrar_historial()
        elif "estadísticas" in entrada_l or "estadisticas" in entrada_l:
            resultado = self.mostrar_estadisticas()
        else:
            resultado = self.generar_respuesta(entrada)

        self.historial.append({
            "dia": self.dia,
            "entrada": entrada,
            "respuesta": resultado
        })
        self.guardar_memoria()

        if self.idioma != "es":
            resultado = traducir_texto(resultado, self.idioma)

        return resultado

    def generar_respuesta(self, entrada):
        plantillas = {
            "amigable": ["¡Qué interesante!", "Cuéntame más.", "Estoy contigo 😊"],
            "formal": ["Gracias por su mensaje.", "Procesando solicitud.", "Estoy a su disposición."],
            "sabia": ["El conocimiento es poder.", "Todo tiene una razón...", "Veamos más allá de lo evidente."],
            "divertida": ["¡Eso me hizo reír! 😂", "Me gusta tu estilo.", "¡Vamos a descubrir más!"]
        }
        return plantillas.get(self.personalidad, plantillas["amigable"])[0]

    def mostrar_historial(self):
        ultimos = self.historial[-5:]
        return "\n".join([f"{h['entrada']} → {h['respuesta']}" for h in ultimos])

    def mostrar_estadisticas(self):
        return f"📊 Mensajes: {self.stats['mensajes']} | 🔍 Busquedas: {self.stats['busquedas']} | 🔄 Reinicios: {self.stats['reinicios']}"

    def reiniciar(self):
        self.historial = []
        self.stats["reinicios"] += 1
        self.guardar_memoria()

    def procesar_archivo(self, filename):
        texto = extraer_texto_archivo(filename)
        if texto:
            self.historial.append({
                "dia": self.dia,
                "entrada": f"Archivo cargado: {filename}",
                "respuesta": texto[:300] + "..." if len(texto) > 300 else texto
            })
            self.guardar_memoria()
            return "Archivo procesado correctamente. Puedes preguntarme sobre su contenido."
        return "No pude leer el archivo o estaba vacío."
