from app.auth import JWTBearer, generate_token


def test_token_validation():
    token = generate_token()
    assert JWTBearer().validate_token(token=token) == True
