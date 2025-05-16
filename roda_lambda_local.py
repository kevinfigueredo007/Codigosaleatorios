import argparse
import json
import importlib.util
import os
import sys

def parse_key_value_string(s):
    """Converte uma string key=value&key2=value2 para dict."""
    if not s:
        return None
    return dict(pair.split("=") for pair in s.split("&") if "=" in pair)

def load_lambda_handler(script_path):
    if not os.path.exists(script_path):
        print(f"Erro: script '{script_path}' não encontrado.")
        sys.exit(1)

    module_name = os.path.splitext(os.path.basename(script_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, "lambda_handler"):
        print(f"Erro: o arquivo '{script_path}' não possui uma função chamada 'lambda_handler'.")
        sys.exit(1)

    return module.lambda_handler

def main():
    parser = argparse.ArgumentParser(description="Executa uma função Lambda localmente com um evento REST API Gateway.")
    parser.add_argument("--script", "-s", required=True, help="Caminho para o script Python que contém a função lambda_handler")
    parser.add_argument("--method", "-m", required=True, help="Método HTTP (ex: GET, POST)")
    parser.add_argument("--path", "-p", required=True, help="Path da requisição (ex: /produtos/123)")
    parser.add_argument("--headers", help="Headers no formato key1=val1&key2=val2")
    parser.add_argument("--query", help="Query strings no formato key1=val1&key2=val2")
    parser.add_argument("--pathParams", help="Path parameters no formato key1=val1&key2=val2")
    parser.add_argument("--body", help="Body da requisição em JSON")

    args = parser.parse_args()

    lambda_handler = load_lambda_handler(args.script)

    headers = parse_key_value_string(args.headers)
    query_params = parse_key_value_string(args.query)
    path_params = parse_key_value_string(args.pathParams)

    try:
        body_data = json.loads(args.body) if args.body else None
    except json.JSONDecodeError:
        print("Erro: body inválido. Certifique-se de que seja um JSON válido.")
        return

    event = {
        "resource": args.path,
        "path": args.path,
        "httpMethod": args.method.upper(),
        "headers": headers,
        "queryStringParameters": query_params,
        "pathParameters": path_params,
        "body": json.dumps(body_data) if body_data else None,
        "isBase64Encoded": False,
    }

    print("\n### Evento Gerado ###")
    print(json.dumps(event, indent=2))

    print("\n### Executando função lambda... ###")
    try:
        response = lambda_handler(event, context={})
    except Exception as e:
        print("A Lambda lançou uma exceção:")
        print(f"{type(e).__name__}: {e}")
        return

    print("\n### Resposta da Lambda ###")
    try:
        print(json.dumps(response, indent=2))
    except (TypeError, ValueError):
        print("A resposta não pôde ser serializada em JSON. Imprimindo valor bruto:")
        print(response)

if __name__ == "__main__":
    main()




python run_lambda_local.py \
  --script lambda_function.py \
  --method POST \
  --path /produtos/123 \
  --headers "Content-Type=application/json" \
  --query "categoria=livros" \
  --pathParams "id=123" \
  --body '{"nome": "Livro", "preco": 29.90}'