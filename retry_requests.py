import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Define política de retry
retry_strategy = Retry(
    total=3,                     # Tenta no máximo 5 vezes
    backoff_factor=1,            # Espera 1s, 2s, 4s, 8s, etc.
    status_forcelist=[429, 500, 502, 503, 504],  # Códigos que devem causar retry
    allowed_methods=["GET", "POST"]             # Métodos permitidos para retry
)

# Adiciona o retry ao adapter
adapter = HTTPAdapter(max_retries=retry_strategy)

# Cria sessão e aplica o adapter
session = requests.Session()
session.mount("https://", adapter)
session.mount("http://", adapter)

# Usa a sessão com retry
try:
    response = session.get("https://httpstat.us/500")  # Simula erro
    print("Status:", response.status_code)
except requests.exceptions.RequestException as e:
    print("Erro na requisição:", e)
