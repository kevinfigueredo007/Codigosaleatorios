class APIException(Exception):
    status_code = 500
    message = "Erro interno"

    def __init__(self, message=None):
        if message:
            self.message = message
        super().__init__(self.message)

    def to_dict(self):
        return {
            "message": self.message
        }

class BadRequestException(APIException):
    status_code = 400
    message = "Requisição inválida"

class UnprocessableEntityException(APIException):
    status_code = 422
    message = "Entidade não processável"

class NotFoundException(APIException):
    status_code = 404
    message = "Recurso não encontrado"
