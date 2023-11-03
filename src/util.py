from custom_encoder import CustomEnconder
import json

def buildResponse(statusCode,headers,body=None):
    responseObject = {
        'statusCode' : statusCode,
        'headers': headers
    }
    if body is not None:
        responseObject['body'] = json.dumps(body,cls=CustomEnconder)
    return responseObject 

