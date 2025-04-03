import random
import string

from starlette.requests import Request


def get_ip_and_forwarded_for(request: Request) -> [str, str]:
    real_ip = request.client.host
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for is not None:
        forwarded_for = real_ip + ", " + forwarded_for
    else:
        forwarded_for = real_ip
    return real_ip, forwarded_for


def generate_random_string(length: int, first_letter: bool = False) -> str:
    if not first_letter:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return random.choice(string.ascii_letters) + ''.join(random.choices(string.ascii_letters + string.digits, k=length-1))

