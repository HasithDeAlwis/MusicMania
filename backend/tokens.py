import jwt
import os
from dotenv import load_dotenv

load_dotenv()

def encode_user(email: str) -> str:
    """
    encode user payload as a jwt
    :param user:
    :return:
    """
    encoded_data = jwt.encode(payload={"email": email},
                              key=os.getenv("WEB_TOKEN"),
                              algorithm="HS256")
    return encoded_data


def decode_user(token: str):
    """
    :param token: jwt token
    :return:
    """
    decoded_data = jwt.decode(jwt=token,
                              key=os.getenv("WEB_TOKEN"),
                              algorithms=["HS256"])

    return decoded_data