from jsonschema import validate


schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "http://example.com/product.schema.json",
  "type": "object",
  "title": "Product Schema",
  "description": "Schema for a product with location info",
  "required": ["name", "price", "region", "capital", "timezones"],
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


body = {
        "name": "Eggs", 
        "price" : 34.99,
        "region" : "Africa",
        "capital" : "Cairo",
        "timezones" : ["UTC+2"]
       }



validate(instance=body, schema=schema)  
