import csv
import re
from collections import Counter


INPUT_FILE = "data/titulares_elecciones_raw.csv"
OUTPUT_LIMPIO = "data/titulares_elecciones_limpio.csv"
OUTPUT_TOP = "data/top_palabras_elecciones.csv"


STOPWORDS = [
    "de", "la", "el", "y", "en", "a", "del", "los", "las",
    "por", "para", "con", "un", "una", "al", "sobre",
    "que", "tras", "entre" , "pero" , "como"
]


TEMAS = {
    "Keiko Fujimori": ["keiko", "fujimori"],
    "Rafael López Aliaga": ["aliaga", "lópez aliaga", "lopez aliaga"],
    "Mario Vizcarra": ["vizcarra"],
    "Carlos Álvarez": ["carlos álvarez", "alvarez"],
    "Alfonso López-Chau": ["lópez-chau", "lopez-chau", "chau"],

    "Instituciones electorales": ["onpe", "jne", "reniec"],
    "Congreso": ["congreso", "parlamento"],
    "Partidos políticos": ["partido", "fuerza popular", "perú libre"]
}


def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r"[^\w\s]", "", texto)
    return texto


def tokenizar(texto):
    palabras = texto.split()
    palabras_limpias = [
        p for p in palabras
        if p not in STOPWORDS and len(p) > 2
    ]
    return palabras_limpias


def clasificar_tema(texto):
    texto = texto.lower()

    for tema, palabras_clave in TEMAS.items():
        for palabra in palabras_clave:
            if palabra in texto:
                return tema

    return "Otros"


def cargar_datos(filename):
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def guardar_csv(data, filename, fieldnames):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def main():
    datos = cargar_datos(INPUT_FILE)

    vistos = set()
    datos_limpios = []
    contador_palabras = Counter()

    for fila in datos:
        titular_original = fila["titular"].strip()

        if titular_original in vistos:
            continue
        vistos.add(titular_original)

        texto_limpio = limpiar_texto(titular_original)
        tokens = tokenizar(texto_limpio)
        tema = clasificar_tema(titular_original)

        for token in tokens:
            contador_palabras[token] += 1

        datos_limpios.append({
            "fecha_extraccion": fila["fecha_extraccion"],
            "titular": titular_original,
            "tema": tema,
            "tokens": " ".join(tokens),
            "url": fila["url"]
        })

    guardar_csv(
        datos_limpios,
        OUTPUT_LIMPIO,
        ["fecha_extraccion", "titular", "tema", "tokens", "url"]
    )

    top_palabras = []
    for palabra, conteo in contador_palabras.most_common(30):
        top_palabras.append({
            "palabra": palabra,
            "frecuencia": conteo
        })

    guardar_csv(
        top_palabras,
        OUTPUT_TOP,
        ["palabra", "frecuencia"]
    )

    print("Proceso completo.")
    print(f"- {len(datos_limpios)} titulares limpios guardados.")
    print("- Top palabras generado.")


if __name__ == "__main__":
    main()