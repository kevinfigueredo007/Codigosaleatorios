from opa_client.opa import OpaClient

client = OpaClient(
    host="localhost",
    port=8181,
    ssl=True,
    headers={
        "Authorization": "Bearer meu-token"
    }
)

client._session.verify = "/home/kevin/awx/project/opa/public.crt"

result = client.query_rule(
    input_data={
            "user": "joao"
        },
    package_path="authz",
    rule_name="allow"
)

print(result)