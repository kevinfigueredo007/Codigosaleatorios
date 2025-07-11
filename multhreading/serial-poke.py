import os
import time
import requests

API_LISTA = "https://pokeapi.co/api/v2/pokemon?limit=1000"
PASTA_SAIDA = "sprites"

def main() -> None:
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    inicio = time.perf_counter()

    # 1. Buscar a lista dos Pokémon
    print("🔍 Buscando lista de Pokémon…")
    resp = requests.get(API_LISTA, timeout=10)
    resp.raise_for_status()
    pokemons = resp.json()["results"]
    print(f"📦 Total recebido: {len(pokemons)}")

    # 2. Para cada Pokémon: obter URL do sprite e baixar
    for i, poke in enumerate(pokemons, 1):
        nome, url_detalhes = poke["name"], poke["url"]

        try:
            det = requests.get(url_detalhes, timeout=5).json()
            sprite_url = det["sprites"]["front_default"]
            if not sprite_url:
                print(f"[{i:>4}] {nome:<12} — sem sprite, pulando")
                continue

            img = requests.get(sprite_url, timeout=10)
            with open(f"{PASTA_SAIDA}/{nome}.png", "wb") as f:
                f.write(img.content)
            print(f"[{i:>4}] {nome:<12} — OK")

        except (requests.RequestException, KeyError) as e:
            print(f"[{i:>4}] {nome:<12} — ERRO: {e}")

    fim = time.perf_counter()
    print(f"\n✅ Concluído em {fim - inicio:.2f} s")

if __name__ == "__main__":
    main()
