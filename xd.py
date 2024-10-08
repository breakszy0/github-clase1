import tkinter as tk
import requests
from io import BytesIO
from PIL import Image, ImageTk
import random

def buscar_poke(numero_pokemon):
    url = f"https://pokeapi.co/api/v2/pokemon/{numero_pokemon}/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        nombre = data["name"].capitalize()
        numero = data["id"]
        tipos = [tipo["type"]["name"] for tipo in data["types"]]
        stats = [stats["base_stat"] for stats in data["stats"]]

        # Obtener la estadística de ataque del Pokémon
        velocidad = stats[0]
        ataque = stats[1]
        defensa = stats[2]

        resultado = f"Nombre: {nombre}\nNúmero: {numero}\nTipo(s): {', '.join(tipos)}\nAtaque: {ataque}\nVelocidad: {velocidad}\nDefensa: {defensa}"

        imagen_url = data["sprites"]["front_default"]
        response_image = requests.get(imagen_url)
        imagen = Image.open(BytesIO(response_image.content))
        imagen = imagen.resize((300, 300), Image.Resampling.LANCZOS)
        foto = ImageTk.PhotoImage(imagen)
        label_imagen.config(image=foto)
        label_imagen.image = foto
    else:
        resultado = "No se encontró el Pokémon. ¡Sigue cazando!"
        label_imagen.config(image=None)

    label_resultado.config(text=resultado)

def mostrar_pokemon_aleatorio():
    total_pokemon = 898  # Actualmente hay 898 Pokémon en la API
    numero_aleatorio = random.randint(1, total_pokemon)
    buscar_poke(numero_aleatorio)

def limpiar_resultado():
    label_resultado.config(text="")
    label_imagen.config(image=None)
    entry_pokemon.delete(0, tk.END)

window = tk.Tk()
window.title("Encuentra tu Pokémon")

entry_pokemon = tk.Entry(window)
entry_pokemon.pack()

button_buscar = tk.Button(window, text="Buscar", command=buscar_poke)
button_buscar.pack()

button_pokemon_aleatorio = tk.Button(window, text="Pokémon Aleatorio", command=mostrar_pokemon_aleatorio)
button_pokemon_aleatorio.pack()

button_limpiar = tk.Button(window, text="Limpiar", command=limpiar_resultado)
button_limpiar.pack()

label_resultado = tk.Label(window, text="")
label_resultado.pack()

label_imagen = tk.Label(window)
label_imagen.pack()

window.mainloop()