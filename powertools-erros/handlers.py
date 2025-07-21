from exceptions import BadRequestException, NotFoundException
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.router import Router
router = Router()

@router.get("/produto/<id>")
def get_produto(id: str):
    if not id.isnumeric():
        raise BadRequestException("ID precisa ser numérico")

    if id != "42":
        raise NotFoundException("Produto não encontrado")

    return {"id": id, "nome": "Produto X"}
