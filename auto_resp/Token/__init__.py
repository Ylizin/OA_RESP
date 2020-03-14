import json
import requests
from .secret import APP_ID,SECRET


TOKEN_URL = r'https://api.weixin.qq.com/cgi-bin/ \
            token?grant_type=client_credential&appid={}&secret={}'\
            .format(APP_ID,SECRET)



class __TOKEN_ACCESSOR:
    def __init__(self):
        super().__init__()
        self.__token = ''
    
    @property
    def token(self):
        return self.__token

    # @token.setter
    # no setter for it 
    
