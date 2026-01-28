import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import re

URL = "https://larepublica.pe/elecciones"


def eliminar_autor(texto):
    """
    Elimina nombres de autor al final del titular.
    Detecta secuencias de 2 a 4 palabras con mayúscula inicial (nombres propios).
    """
    texto = texto.replace("\n", " ").strip()

    # Patrón: Nombre Apellido / Nombre Apellido Apellido
    patron_autor = r"(.*?)([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})$"

    match = re.match(patron_autor, texto)

    if match:
        posible_titular = match.group(1).strip()

        # Evitamos cortar titulares muy cortos por error
        if len(posible_titular) > 40:
            return posible_titular

    return texto


def extraer_titulares(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    titulares = []

    enlaces = soup.find_all("a")

    for a in enlaces:
        texto = a.get_text(strip=True)
        link = a.get("href")

        if not texto or not link:
            continue

        if len(texto) < 60:
            continue

        texto_limpio = eliminar_autor(texto)

        if len(texto_limpio) < 40:
            continue

        if link.startswith("/"):
            link = "https://larepublica.pe" + link

        titulares.append({
            "fecha_extraccion": datetime.now().strftime("%Y-%m-%d"),
            "titular": texto_limpio,
            "url": link
        })

    return titulares


def guardar_csv(data, filename):
    if not data:
        print("No se extrajeron datos. CSV no generado.")
        return

    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def main():
    datos = extraer_titulares(URL)
    guardar_csv(datos, "data/titulares_elecciones_raw.csv")
    print(f"OK: {len(datos)} titulares guardados.")


if __name__ == "__main__":
    main()