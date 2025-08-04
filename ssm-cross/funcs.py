import boto3, time

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
ssm_cross = boto3.client('ssm',
         aws_access_key_id=credentials["AccessKeyId"],
         aws_secret_access_key=credentials["SecretAccessKey"],
         aws_session_token=credentials["SessionToken"],
     )


def start_automation(account_id, region, document_name, parameters):

    arn_assume_role = 'arn:aws:iam::046219898673:role/lambda-administration-role'
    
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
    response = ssm_cross.describe_automation_step_executions(
        AutomationExecutionId=execution_id
    )
    return str(response)

def stop_automation(execution_id):
    response = ssm.stop_automation_execution(
        AutomationExecutionId=execution_id
    )
    return response

def describe_automation_executions():
    response = ssm_cross.describe_automation_executions(
        MaxResults=50
    )
    return str(response)

def share_document(account_id, document_name, adicionar=True):
    if adicionar:
        response = ssm.modify_document_permission(
            Name=document_name,
            PermissionType='Share',
            AccountIdsToAdd=account_id
        )
    else:
        response = ssm.modify_document_permission(
            Name=document_name,
            PermissionType='Share',
            AccountIdsToRemove=account_id
        )
    return response

def list_shared_accounts(document_name):
    response = ssm.describe_document_permission(
        Name=document_name,
        PermissionType='Share'
    )
    return response.get('AccountIds', [])


def executar_comando_ssm(instance_id, comando, comentario="Execução via boto3"):
    try:
        response = ssm.send_command(
            InstanceIds=[instance_id],
            DocumentName="AWS-RunShellScript",
            Parameters={"commands": [comando]},
            Comment=comentario,
        )

        command_id = response["Command"]["CommandId"]
        print(f"Comando enviado com ID: {command_id}")

        while True:
            time.sleep(2)
            output = ssm.get_command_invocation(
                CommandId=command_id,
                InstanceId=instance_id
            )

            if output["Status"] in ("Success", "Failed", "Cancelled", "TimedOut"):
                break

        return {
            "Status": output["Status"],
            "StandardOutputContent": output.get("StandardOutputContent", ""),
            "StandardErrorContent": output.get("StandardErrorContent", "")
        }

    except Exception as e:
        return {"error": str(e)}


