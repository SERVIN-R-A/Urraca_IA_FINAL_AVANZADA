import os
import wikipedia
from deep_translator import GoogleTranslator

def buscar_en_internet(tema, idioma="es"):
    try:
        wikipedia.set_lang(idioma)
        resumen = wikipedia.summary(tema, sentences=2)
        return resumen
    except Exception:
        return "No encontré resultados claros sobre eso."

def traducir_texto(texto, destino="es"):
    try:
        return GoogleTranslator(source="auto", target=destino).translate(texto)
    except Exception as e:
        return texto

def extraer_texto_archivo(ruta):
    if ruta.endswith(".txt"):
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""
    elif ruta.endswith(".pdf"):
        try:
            import PyPDF2
            texto = ""
            with open(ruta, "rb") as f:
                lector = PyPDF2.PdfReader(f)
                for pagina in lector.pages:
                    texto += pagina.extract_text() or ""
            return texto
        except Exception:
            return ""
    else:
        return ""
