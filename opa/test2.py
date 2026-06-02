import requests

r = requests.get(
    "https://localhost:8181/v1/data",
    verify="/home/kevin/awx/project/opa/public.crt",
    headers={
        "Authorization": "Bearer meu-token"
    },
)

print(r.status_code)
print(r.text)