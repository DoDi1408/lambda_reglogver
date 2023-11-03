import json
from auth import *
from util import buildResponse
from user import *
from restaurants import *
from promotions import *
#default headers:
headers = {
            'Content-Type' :'application/json',
            'Access-Control-Allow-Origin' : '*'
}


def lambda_handler(event, context):
    
    ## setting logging for cloudwatch
    logger.info(event)
    ##creating things i have to access
    message = event['body'] 
    event_headers = event['headers'] ##headers of the event
    
    queryParams = event['queryStringParameters'] ##url parameters
    multiqueryParams = event['multiValueQueryStringParameters'] ## url multi parameters
    pathParams = event['pathParameters']

    sourceIp = event_headers['X-Forwarded-For'] #ip source request
    
    path = event['resource'] ##event path like /user/register or /user
    httpMethod = event['httpMethod'] ##request httpMethod
    
    ##method to test that the api is working and a connection to the database has been established
    if httpMethod == 'GET' and path == '/health':
        response = buildResponse(200, headers, {'message': 'Health Check', 'parameters': queryParams})

    elif httpMethod == 'POST' and path == '/user/register':

        if message is None:
            return buildResponse(401, headers, {'message':'Empty body'})
        data = json.loads(message) ##message is the body of the api request

        if 'username' in data and 'user_email' in data and 'user_password' in data:
            nombre = data['username']
            email = data['user_email']
            contraseña = data['user_password']
        else:
            return buildResponse(401,headers,{'message' :'All fields requiered'})
        
        if getUserByEmail(email):
            return buildResponse(401,headers,{'message' :'Email is already in use'})
        
        response = createUser(nombre,email,contraseña,headers)

    elif httpMethod == 'POST' and path == '/user/login':

        if message is None:
            return buildResponse(401, headers, {'message':'Empty body'})
        data = json.loads(message) ##message is the body of the api request

        if 'user_email' in data and 'user_password' in data:
            email = data['user_email']
            contraseña = data['user_password']
        else:
            return buildResponse(401,headers,{'message' :'All fields requiered'})
        
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT contraseña_usuario FROM usuarios WHERE email_usuario = %s", (email,))
                stored_password_hash = cur.fetchone()
                contraseña_bytes = contraseña.encode('utf-8')
                if stored_password_hash:
                    stored_password_hash = stored_password_hash[0]
                    if hashlib.blake2b(contraseña_bytes).hexdigest() == stored_password_hash:
                        del stored_password_hash
                        user = getUserByEmail(email)
                        accessToken = generateToken(user[1],user[0],user[2],sourceIp)
                        response = buildResponse(200,headers, {'access-token': accessToken})
                    else:
                        return buildResponse(403,headers,{'message': 'Invalid Credentials'})
                else:
                    return buildResponse(403,headers,{'message': 'Invalid Credentials'})
        except Exception as e:
            return buildResponse(500,headers,{'message': "DB Server Error :("})
        
    elif httpMethod == 'POST' and path == '/verify':
        
        if 'access-token' in event_headers:
            token = event_headers['access-token']
        else:
            return buildResponse(401,headers,{'message' :'All fields requiered'})
        
        body = authenticateToken(token,sourceIp)
        if body['verified'] == True:
            response = buildResponse(200,headers,body)
        else:
            response = buildResponse(400,headers,body)
    elif httpMethod == 'PATCH' and path == '/user':

        if message is None:
            return buildResponse(401, headers, {'message':'Empty body'})
        data = json.loads(message) ##message is the body of the api request

        if 'access-token' in event_headers and 'new_name' in data and 'new_email' in data and 'new_password' in data:
            token = event_headers['access-token']
            nombre = data['new_name']
            nuevo_email = data['new_email']
            contraseña = data['new_password']
        else:
            return buildResponse(401,headers,{'message' :'All fields requiered'})
        
        result = authenticateToken(token,sourceIp)

        token = result['accessToken']
        id = result['id']
        headers['access-token'] = token

        if result['verified'] == True:
            if getUserByEmail(result['email']) is None:
                return buildResponse(404,headers,{'message' :'Not Found in Database'})
            response = updateUserByEmail(nombre,nuevo_email,contraseña,id,headers)
        else:
            response = buildResponse(403,headers,{'message' : result['message']})

    elif httpMethod == 'PATCH' and path == '/user/addPoints/{points}':
        points = pathParams['points']

        if 'access-token' in event_headers:
            token = event_headers['access-token']
        else:
            return buildResponse(401,headers,{'message' :'No JWT Token'})
        
        result = authenticateToken(token,sourceIp)
        token = result['accessToken']
        headers['access-token'] = token
        id = result['id']
        if result['verified'] == True:
            response = addPoints(id,points,headers)
        else:
            response = buildResponse(403,headers,{'message' : result['message']})

    elif httpMethod == 'GET' and path == '/user':
        if 'access-token' in event_headers:
            token = event_headers['access-token']
        else:
            return buildResponse(401,headers,{'message' :'No JWT Token'})

        result = authenticateToken(token,sourceIp)
        token = result['accessToken']
        headers['access-token'] = token

        if result['verified'] == True:
            user = getUserByEmail(result['email'])
            if user is None:
                buildResponse(404, headers,{'message': 'User Not Found'})
            else:
                response = buildResponse(200,headers,{'id':user[0],'nombre':user[2],'email':user[1],'puntos':user[3]})
        else:
            response = buildResponse(403,headers,{'message' : result['message']})

    elif httpMethod == 'GET' and path == '/restaurants':
        if 'access-token' in event_headers:
            token = event_headers['access-token']
        else:
            return buildResponse(401,headers,{'message' :'No JWT Token'})

        result = authenticateToken(token,sourceIp)
        token = result['accessToken']
        headers['access-token'] = token

        if result['verified'] == True:
            response = getRestaurants(headers)
        else:
            response = buildResponse(403,headers,{'message' : result['message']})

    elif httpMethod == 'GET' and path == '/promotions':

        if 'access-token' in event_headers:
            token = event_headers['access-token']
        else:
            return buildResponse(401,headers,{'message' :'No JWT Token'})

        result = authenticateToken(token,sourceIp)
        token = result['accessToken']
        headers['access-token'] = token

        if result['verified'] == True:
            if 'id' in queryParams:
                restaurantes_json = []
                promotions = getRestaurantPromotions(int(id),headers)
                if isinstance(promotions, Exception):
                    return buildResponse(500,headers,{'message': "Error retrieving restaurant with id %s" % id})
                response = promotions
            else:
                response = getPromotions(headers)
        else:
            response = buildResponse(403,headers,{'message' : result['message']})


    else:
        response = buildResponse(404, headers,{'message': 'Not Found'})
    return response


