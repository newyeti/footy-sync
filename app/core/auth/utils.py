from typing import Optional

import jwt
import ssl
import certifi

from fastapi import Depends, HTTPException, status
from fastapi.security import SecurityScopes, HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import get_app_settings

class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = None, **kwargs) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, detail=detail)
    

class UnauthenticatedException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, 
                         detail="Requires authentication")
        
class VerifyToken:
    """Verify token using PyJWT"""
    
    def __init__(self) -> None:
        self.config = get_app_settings().auth0        
        jwks_uri = f'https://{self.config.domain}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(uri=jwks_uri, ssl_context=ssl.create_default_context(cafile=certifi.where()))
    
    def verify(self, 
               security_scope: SecurityScopes,
               token: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer())):
        if token is None:
            raise UnauthenticatedException

        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(
                token.credentials
                ).key
        except jwt.exceptions.PyJWKClientError as error:
            raise UnauthorizedException(str(error))
        except jwt.exceptions.DecodeError as error:
            raise UnauthorizedException(str(error))
        
        
        try:
            payload = jwt.decode(
                jwt=token.credentials,
                key=signing_key,
                algorithms=self.config.algorithm,
                audience=self.config.api_audience,
                issuer=self.config.issuer
            )
            return payload
        
        except Exception as error:
            raise UnauthorizedException(str(error))                
        