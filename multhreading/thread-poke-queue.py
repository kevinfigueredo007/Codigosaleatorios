import os
import requests
import queue
import concurrent.futures

# Diretório para sprites
os.makedirs("sprites", exist_ok=True)

# Filas compartilhadas
fila_pokemons = queue.Queue()
fila_sprites = queue.Queue()

# Quantidade de threads
NUM_PRODUTORES = 30
NUM_CONSUMIDORES = 30

# Função do produtor (executada em threads)
def produtor():
    while True:
        item = fila_pokemons.get()
        if item is None:
            break
        nome, url = item
        try:
            r = requests.get(url, timeout=5)
            sprite_url = r.json()["sprites"]["front_default"]
            if sprite_url:
                fila_sprites.put((nome, sprite_url))
                print(f"[PRODUTOR] {nome} → sprite encontrado")
        except Exception as e:
            print(f"[ERRO-PRODUTOR] {nome}: {e}")
        finally:
            fila_pokemons.task_done()

# Função do consumidor (executada em threads)
def consumidor():
    while True:
        item = fila_sprites.get()
        if item is None:
            break
        nome, sprite_url = item
        try:
            img = requests.get(sprite_url, timeout=10)
            with open(f"sprites/{nome}.png", "wb") as f:
                f.write(img.content)
            print(f"[CONSUMIDOR] {nome} → baixado")
        except Exception as e:
            print(f"[ERRO-CONSUMIDOR] {nome}: {e}")
        finally:
            fila_sprites.task_done()

def main():
    print("🔍 Buscando pokémons...")
    try:
        r = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1000")
        pokemons = r.json()["results"]
    except Exception as e:
        print(f"[ERRO] Falha ao buscar a lista de pokémons: {e}")
        return

    for p in pokemons:
        fila_pokemons.put((p["name"], p["url"]))

    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_PRODUTORES + NUM_CONSUMIDORES) as executor:
        # Iniciar produtores
        for _ in range(NUM_PRODUTORES):
            executor.submit(produtor)

        # Iniciar consumidores
        for _ in range(NUM_CONSUMIDORES):
            executor.submit(consumidor)

        # Esperar a fila de pokémons esvaziar
        fila_pokemons.join()

        # Enviar sinais de parada para produtores
        for _ in range(NUM_PRODUTORES):
            fila_pokemons.put(None)

        # Esperar a fila de sprites esvaziar
        fila_sprites.join()

        # Enviar sinais de parada para consumidores
        for _ in range(NUM_CONSUMIDORES):
            fila_sprites.put(None)

    print("✅ Todos os sprites foram baixados!")

if __name__ == "__main__":
    main()
