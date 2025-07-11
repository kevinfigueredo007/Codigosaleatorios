import aiohttp
import asyncio
import os

# Pasta para salvar os sprites
os.makedirs("sprites", exist_ok=True)

# Limite de conexões simultâneas
MAX_CONEXOES = 100

# Baixa a lista de pokémons (nome + URL de detalhes)
async def buscar_lista_pokemons(session):
    url = "https://pokeapi.co/api/v2/pokemon?limit=1000"
    async with session.get(url) as resp:
        dados = await resp.json()
        return [(p["name"], p["url"]) for p in dados["results"]]

# Busca a URL do sprite
async def obter_sprite_url(session, nome, url_detalhes):
    try:
        async with session.get(url_detalhes) as resp:
            dados = await resp.json()
            return nome, dados["sprites"]["front_default"]
    except Exception as e:
        print(f"[ERRO-SPRITE-URL] {nome}: {e}")
        return nome, None

# Baixa o sprite
async def baixar_sprite(session, nome, sprite_url):
    if sprite_url is None:
        return f"[SKIP] {nome}"
    try:
        async with session.get(sprite_url) as resp:
            conteudo = await resp.read()
            with open(f"sprites/{nome}.png", "wb") as f:
                f.write(conteudo)
        return f"[OK] {nome}"
    except Exception as e:
        return f"[ERRO-DOWNLOAD] {nome}: {e}"

# Função principal
async def main():
    conector = aiohttp.TCPConnector(limit=MAX_CONEXOES)
    timeout = aiohttp.ClientTimeout(total=30)

    async with aiohttp.ClientSession(connector=conector, timeout=timeout) as session:
        print("🔍 Buscando lista de pokémons...")
        pokemons = await buscar_lista_pokemons(session)
        print(f"📦 Total: {len(pokemons)}")

        # Buscar todas as URLs de sprite
        tarefas_sprites = [obter_sprite_url(session, nome, url) for nome, url in pokemons]
        sprites_info = await asyncio.gather(*tarefas_sprites)

        # Baixar todos os sprites em paralelo
        tarefas_downloads = [baixar_sprite(session, nome, sprite_url) for nome, sprite_url in sprites_info]
        for futuro in asyncio.as_completed(tarefas_downloads):
            resultado = await futuro
            print(resultado)

    print("✅ Todos os sprites foram baixados!")

# Rodar
if __name__ == "__main__":
    asyncio.run(main())
