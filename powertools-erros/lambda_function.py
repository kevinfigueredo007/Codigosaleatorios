from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.exceptions import BadRequestError
from aws_lambda_powertools.logging import Logger
from exceptions import APIException
import handlers
from aws_lambda_powertools.event_handler import Response

app = APIGatewayRestResolver()
logger = Logger()

app.include_router(handlers.router)

@app.exception_handler(APIException)
def handle_custom_exceptions(ex: APIException):
    logger.warning(f"Erro tratado: {ex.message}")
    return Response(
        status_code=ex.status_code,
        body=ex.to_dict()
    )

def lambda_handler(event, context):
    return app.resolve(event, context)
