from aws_lambda_powertools.utilities import parameters
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.validation import SchemaValidationError, validate

schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "http://example.com/product.schema.json",
  "title": "Product Schema",
  "description": "Schema for a product with location info",
  "required": ["name", "price", "region", "capital", "timezones"],
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "The name of the product",
      "maxLength": 100
    },
    "price": {
      "type": "number",
      "description": "The price of the product",
      "minimum": 0
    },
    "region": {
      "type": "string",
      "description": "The geographic region"
    },
    "capital": {
      "type": "string",
      "description": "The capital city of the region"
    },
    "timezones": {
      "type": "array",
      "description": "List of timezones",
      "items": {
        "type": "string"
      },
      "minItems": 2
    }
  }
}


def lambda_handler(event, context) -> dict:

    try:
        validate(event=event, schema=schema)
    
    except SchemaValidationError as e:
        return {
            "statusCode": 400,
            "body": {
                "message": "Invalid input",
                "error": str(e),
            },
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": {
                "message": "Internal server error",
                "error": str(e),
            },
        }

    

event = {
        "name": "Eggs", 
        "price" : 34.99,
        "region" : "Africa",
        "capital" : "Cairo",
        "timezones" : ["UTC+2"]
       }

print(lambda_handler(event, None))
