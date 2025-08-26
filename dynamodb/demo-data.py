from boto3.dynamodb.conditions import Key
import boto3
from datetime import datetime, timezone

dynamodb_resource = boto3.resource("dynamodb", endpoint_url="http://localhost:4566")
table = dynamodb_resource.Table("Automacoes")

def now_iso():
    return datetime.now(timezone.utc).isoformat()

# Lista de automações
automacoes = [
    {
        "Id": "001",
        "Nome": "Automação de Pagamentos",
        "Descricao": "Fluxo para processar e conciliar pagamentos",
        "Responsavel": "kevin@example.com"
    },
    {
        "Id": "002",
        "Nome": "Automação de Notificações",
        "Descricao": "Envia notificações via e-mail e SMS",
        "Responsavel": "ana@example.com"
    },
    {
        "Id": "003",
        "Nome": "Automação de Relatórios",
        "Descricao": "Gera relatórios financeiros automaticamente",
        "Responsavel": "carlos@example.com"
    },
    {
        "Id": "004",
        "Nome": "Automação de Monitoramento",
        "Descricao": "Monitora serviços críticos da aplicação",
        "Responsavel": "julia@example.com"
    }
]

for auto in automacoes:
    pk = f"AUTOMACAO#{auto['Id']}"

    # Item de metadata da automação
    table.put_item(
        Item={
            "PK": pk,
            "SK": "METADATA",
            "Type": "AUTOMACAO",
            "Nome": auto["Nome"],
            "Descricao": auto["Descricao"],
            "Status": "ATIVA",
            "Responsavel": auto["Responsavel"],
            "CriadoEm": now_iso(),
            "AtualizadoEm": now_iso()
        }
    )

    # Uma aplicação exemplo por automação
    table.put_item(
        Item={
            "PK": pk,
            "SK": "APLICACAO#01",
            "Type": "APLICACAO",
            "Nome": f"App principal da {auto['Nome']}",
            "Descricao": "Aplicação principal dessa automação",
            "Linguagem": "Python",
            "RepositorioGit": f"https://github.com/org/{auto['Id']}-app",
            "Versao": "v1.0.0",
            "CriadoEm": now_iso()
        }
    )

    # Duas rotas exemplo por automação
    table.put_item(
        Item={
            "PK": pk,
            "SK": "APLICACAO#01#ROTA#001",
            "Type": "ROTA",
            "Path": "/start",
            "MetodoHTTP": "POST",
            "Auth": "JWT",
            "Timeout": 30,
            "Ativo": True,
            "CriadoEm": now_iso()
        }
    )

    table.put_item(
        Item={
            "PK": pk,
            "SK": "APLICACAO#01#ROTA#002",
            "Type": "ROTA",
            "Path": "/status",
            "MetodoHTTP": "GET",
            "Auth": "JWT",
            "Timeout": 10,
            "Ativo": True,
            "CriadoEm": now_iso()
        }
    )

print("✅ Automações 001–004 inseridas com sucesso!")
