import os
import requests
from concurrent.futures import ThreadPoolExecutor

# Criar a pasta onde os sprites serão salvos
os.makedirs("sprites", exist_ok=True)

MAX_WORKERS = 40  # Número máximo de threads

# 1. Buscar os Pokémon
def buscar_pokemons(limit=1000):
    url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["results"]  # lista de dicts com name e url

# 2. Obter o sprite de um pokémon
def obter_sprite_url(pokemon):
    response = requests.get(pokemon["url"])
    response.raise_for_status()
    data = response.json()
    sprite_url = data["sprites"]["front_default"]
    return (pokemon["name"], sprite_url)

# 3. Fazer download do sprite
def baixar_sprite(nome_e_url):
    nome, url = nome_e_url
    if url:
        response = requests.get(url)
        response.raise_for_status()
        with open(f"sprites/{nome}.png", "wb") as f:
            f.write(response.content)
        print(f"{nome} salvo com sucesso.")
    else:
        print(f"{nome} não possui sprite.")

# Fluxo principal
if __name__ == "__main__":
    print("Buscando lista de pokémons...")
    pokemons = buscar_pokemons()

    print("Obtendo URLs dos sprites...")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        sprites = list(executor.map(obter_sprite_url, pokemons))

    print("Baixando sprites...")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(baixar_sprite, sprites)

    print("Finalizado.")
