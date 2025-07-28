import json
from time import sleep
from time import sleep
from funcs import start_automation, get_automation_execution, describe_automation_step_executions, describe_automation_executions, share_document, stop_automation, list_shared_accounts


def lambda_handler(event, context):
    
    event = json.loads(event['body'])
    print("evento: ", event)

    if event.get('senha') != '0a532dfb-9ff4-47f8-a4d3-4ce6b832a477':
        return {
            'statusCode': 401,
            'body': json.dumps({"error": "Unauthorized"})
        }

    try:
    
        account_id = event.get('account_id')
        region = event.get('region')
        document_name = event.get('document_name')
        parameters = event.get('parameters')
        execution_id = event.get('execution_id')
        action = event.get('action')
        print("action: ", action)

        

        match action:
            case 'start_automation':
                response = start_automation(account_id, region, document_name, parameters)
            case 'stop_automation':
                response = stop_automation(execution_id)
            case 'get_execution':
                execution_id = get_automation_execution(execution_id)
                response = describe_automation_step_executions(execution_id)
            case 'share_document':
                adicionar = event.get('adicionar')
                response = share_document(account_id, document_name, adicionar)
            case 'list_shared_accounts':
                response = list_shared_accounts(document_name)

            case _:
                raise ValueError(f"Invalid action: {action}")
        

        #response = describe_automation_executions()
        
        #sleep(6)
        #response = stop_automation(response)

        # Retorna o ID da execução
        return {
            'statusCode': 200,
            'body': {
                "message": "SSM Automation execution started successfully.",
                "automation_execution_id": response
            }
        }
        
    except KeyError as e:
        print(f"Erro: O evento de entrada está faltando a chave {e}.")
        return {
            'statusCode': 400,
            'body': json.dumps({"error": f"Missing key in event payload: {e}"})
        }
    except Exception as e:
        print(f"Ocorreu um erro ao iniciar a automação: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({"error": f"Failed to start SSM automation: {str(e)}"})
        }


