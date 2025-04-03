import datetime

from pydantic import BaseModel


class TokensPairDTO(BaseModel):
    access_token: str
    access_token_expires: datetime.datetime
    refresh_token: str
    refresh_token_expires: datetime.datetime
