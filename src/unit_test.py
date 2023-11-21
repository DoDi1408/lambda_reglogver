import pytest
from verification import *
from user import *
from auth import *
from restaurants import *
from promotions import *
from donation import *
from datetime import datetime, timedelta

headers = {
            'Content-Type' :'application/json',
            'Access-Control-Allow-Origin' : '*'
}

#testing function to get existing user using test@test.com, an email in our database
def test_getUserByEmail_existing_user():
    email = 'test@test.com'
    user = getUserByEmail(email)
    assert user is not None

#testing function to get a non-existing user using an email not in our database
def test_getUserByEmail_nonexistent_user():
    email = 'nonexistent@test.com'
    user = getUserByEmail(email)
    assert user is None

# Test verifyEmail with an invalid token
def test_verifyEmail_invalid_token():
    sourceIp = "192.168.1.1"
    verify_result = verifyEmail("invalid_token", sourceIp)
    expected_result = {'verified': False, 'message': 'Invalid Token'}
    assert verify_result == expected_result

# test verify email with valid token and ip
def test_verifyEmail_valid_token_and_ip():
    email = "test@test.com"
    sourceIp = "192.168.1.1"

    # Create a valid token
    valid_token = createVerifyToken(email, sourceIp)

    #verify with valid ip
    result = verifyEmail(valid_token, sourceIp)

    assert result['verified'] is True
    assert result['message'] == "Successfully verified user in database"

#test verify with invalid ip
def test_verifyEmail_invalid_ip():
    email = "test@test.com"
    valid_sourceIp = "192.168.1.1"
    invalid_sourceIp = "192.168.1.2"

    # Create a valid token
    valid_token = createVerifyToken(email, valid_sourceIp)

    # try to verify from invalid source
    result = verifyEmail(valid_token, invalid_sourceIp)

    assert result['verified'] is False
    assert result['message'] == "Ip Not Valid"

#testing token creation
def test_createVerifyToken_valid_input():
    email = "test@example.com"
    sourceIp = "192.168.1.1"

    #create token
    token = createVerifyToken(email, sourceIp)

    assert token is not None

#testing token incorrect creation
def test_createVerifyToken_invalid_input():
    email = "test@example.com"
    sourceIp = None
    #create invalid token
    token = createVerifyToken(email, sourceIp)
    assert token is None

#testing updating user
def test_updateUserById():
    nuevo_nombre = "Updated Test User"
    nuevo_email = "test@test.com"
    nueva_contraseña = "new_password"
    user_id = 1
    # Call the updateUserById function
    response = updateUserById(nuevo_nombre, nuevo_email, nueva_contraseña, user_id, headers)

    # Assert the response status code is 200
    print(response['body'])
    assert response['statusCode'] == 200

#testing failure
def test_updateUserById_failure():
    nuevo_nombre = "Updated Test User"
    nuevo_email = "test@test.com"
    nueva_contraseña = "new_password"
    user_id = 999  # Use an invalid user ID to trigger an error

    # Call the updateUserById function
    response = updateUserById(nuevo_nombre, nuevo_email, nueva_contraseña, user_id, headers)

    # Assert the response status code is 500 (indicating an internal server error)
    assert response['statusCode'] == 500

    # Assert the response body contains an error message
    assert 'error' in response['body']

def test_updateUserByIdNoPassword_success():
    nuevo_nombre = "Updated Test User"
    nuevo_email = "test@test.com"
    user_id = 1

    # Call the function
    response = updateUserByIdNoPassword(nuevo_nombre, nuevo_email, user_id, headers)
    # Assert the response
    assert response['statusCode'] == 200

def test_updateUserByIdNoPassword_failure():
    id_to_update = 999
    nuevo_nombre = "Updated Test User"
    nuevo_email = "test@test.com"

    # call functions
    response = updateUserByIdNoPassword(nuevo_nombre, nuevo_email, id_to_update, headers)

    # Assert the response status code is 500 (indicating an internal server error)
    assert response['statusCode'] == 500

    # Assert the response body contains an error message
    assert 'error' in response['body']


def test_authenticateToken_invalid_ip():
    # Generate a valid token
    valid_email = "test@example.com"
    valid_user_id = "123"
    valid_nombre = "John Doe"
    valid_source_ip = "127.0.0.1"
    valid_token = generateToken(valid_email, valid_user_id, valid_nombre, valid_source_ip)

    # Authenticate with an invalid IP
    invalid_ip = "192.168.0.1"
    result = authenticateToken(valid_token, invalid_ip)

    # Assert that the verification fails due to an invalid IP
    assert result['verified'] is False
    assert result['message'] == 'Ip Not Valid'
    assert result['accessToken'] == valid_token

def test_authenticateToken_invalid_token():
    # Authenticate with an invalid token
    invalid_token = "invalid_token"
    result = authenticateToken(invalid_token, "127.0.0.1")

    # Assert that the verification fails due to an invalid token
    assert result['verified'] is False
    assert result['message'] == 'Invalid Token'
    assert result['accessToken'] == invalid_token

def test_authenticateToken_expired_token():
    # Generate an expired token
    expired_email = "test@example.com"
    expired_user_id = "123"
    expired_nombre = "John Doe"
    expired_source_ip = "127.0.0.1"
    expired_token_data = {'email': expired_email, 'id': expired_user_id, 'nombre': expired_nombre,
                          'sourceIp': expired_source_ip, 'exp': datetime.utcnow() - timedelta(hours=1)}
    expired_token = jwt.encode(expired_token_data, 'LEMAO', algorithm='HS256')

    # Authenticate with an expired token
    result = authenticateToken(expired_token, "127.0.0.1")

    # Assert that the verification fails due to an expired token
    assert result['verified'] is False
    assert result['message'] == 'Token Expired'
    assert result['accessToken'] == expired_token

##testing restaurants
def test_getRestaurants_success():
    # Call the function
    response = getRestaurants(headers)

    # Assert the status code
    assert response['statusCode'] == 200

def test_getDonationsByUserId_success():
    user_id = 1

    response = getDonationsByUserId(user_id, headers)

    # Assert the status code
    assert response['statusCode'] == 200

#get promotions by restaurants
def test_getRestaurantPromotions_success():
    restaurant_id = 1

    # Call the function
    response = getRestaurantPromotions(restaurant_id, headers)

    # Assert the status code
    assert response['statusCode'] == 200

#get promotions all
def test_getPromotions_success():

    # Call the function
    response = getPromotions(headers)

    # Assert the status code
    assert response['statusCode'] == 200

if __name__ == "__main__":
    pytest.main()