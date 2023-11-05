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

def renderHtmlResponse(title, message):
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': f'''
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{title}</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        text-align: center;
                        background-color: #f4f4f4;
                    }}
                    .container {{
                        margin: 100px auto;
                        max-width: 600px;
                        padding: 20px;
                        background-color: #fff;
                        border-radius: 10px;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    }}
                    h1 {{
                        color: #333;
                    }}
                    p {{
                        font-size: 18px;
                        color: #555;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>{title}</h1>
                    <p>{message}</p>
                </div>
            </body>
            </html>
        ''',
    }