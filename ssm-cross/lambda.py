import json
import boto3

def assume_role(role_arn):
    sts_client = boto3.client('sts')
    assumed_role_object = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName="AssumeRoleSession1"
    )
    credentials = assumed_role_object['Credentials']
    return credentials

credentials = assume_role("arn:aws:iam::488367140555:role/poc-ssm-AutomationExecutionRole")

ssm = boto3.client('ssm')
ssm_step = boto3.client('ssm',
         aws_access_key_id=credentials["AccessKeyId"],
         aws_secret_access_key=credentials["SecretAccessKey"],
         aws_session_token=credentials["SessionToken"],
     )


def lambda_handler(event, context):
    try:
    
        account_id = event['account_id']
        region = event['region']
        document_name = event['document_name']
        parameters = event['parameters']
    
        
        #response = start_automation(account_id, region, document_name, parameters)
        execution_id = get_automation_execution("2c2ed008-4d35-4944-ac89-c69999e98dc8")
        response = describe_automation_step_executions(execution_id)

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


def start_automation(account_id, region, document_name, parameters):

    arn_assume_role = 'arn:aws:iam::046219898673:role/service-role/poc-ssm-role-af2gii2a'
    
    print(f"Iniciando a automação do documento: {document_name}...")
    
    # Chama a API StartAutomationExecution
    response = ssm.start_automation_execution(
    DocumentName=document_name,
    DocumentVersion='$DEFAULT',
    Parameters={
        'AutomationAssumeRole': [arn_assume_role],
        'arg1': ["Minha mensagem"],
        'arg2': ['https://sqs.us-east-1.amazonaws.com/488367140555/conta1']
    },
    TargetLocations=[
        {
            'Accounts': [account_id],
            'Regions': [region],
            'ExecutionRoleName': 'poc-ssm-AutomationExecutionRole'
        }
    ]
)
    
    # Pega o ID da execução para o log
    automation_execution_id = response['AutomationExecutionId']
    
    print(f"Automação iniciada com sucesso! ID da Execução: {automation_execution_id}")
    return automation_execution_id

def get_automation_execution(execution_id):
    response = ssm.get_automation_execution(
        AutomationExecutionId=execution_id
    )

    execution = response['AutomationExecution']["StepExecutions"][0]["Outputs"]["ExecutionId"][0]

    #print(execution)
    
    return execution

def describe_automation_step_executions(execution_id):
    response = ssm_step.describe_automation_step_executions(
        AutomationExecutionId=execution_id
    )
    return str(response)
