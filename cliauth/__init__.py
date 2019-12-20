import requests
import jwt
from time import sleep
from typing import NamedTuple

class DeviceAuthConfig(NamedTuple):
    client_id: str = None
    scope: str = None
    audience: str = None
    device_authorization_url: str = None
    oauth_token_url: str = None

def _request_device_code(config: DeviceAuthConfig):
    res = requests.post(
        url=config.device_authorization_url,
        data=dict(
            client_id=config.client_id,
            scope=config.scope,
            audience=config.audience,
        ),
        headers={
            'content-type': "application/x-www-form-urlencoded"
        }
    )

    return res.json()


def _request_token(config: DeviceAuthConfig, device_code: str):
    res = requests.post(
        url=config.oauth_token_url,
        data=dict(
            client_id=config.client_id,
            grant_type="urn:ietf:params:oauth:grant-type:device_code",
            device_code=device_code
        ),
        headers={
            'content-type': "application/x-www-form-urlencoded"
        }
    )

    return res.json()


class DeviceAuthFlow():
    def __init__(self, config: DeviceAuthConfig):
        self.__config = config

        self.__device_code_res = None
        self.__device_code = None
        self.__verification_uri = None
        self.__verification_uri_complete = None
        self.__verification_poll_interval = None
        self.__expiration = None

        self.__token_res = None

    def start(self):
        res = _request_device_code(self.__config)
        self.__device_code = res.get('device_code')
        self.__verification_uri = res.get('verification_uri')
        self.__verification_uri_complete = res.get('verification_uri_complete')
        self.__verification_poll_interval = res.get('interval', 5)
        self.__device_code_res = res
    
    def get_verification_uri_complete(self):
        return self.__verification_uri_complete

    def try_fetch_token(self):
        res = _request_token(self.__config, self.__device_code)
        self.__token_res = res

    def is_verfication_still_valid(self):
        # TODO: real implementation
        return True

    def is_verification_still_pending(self):
        if self.__token_res:
            return 'error' in self.__token_res and self.__token_res['error'] == 'authorization_pending'
        else:
            return True

    def should_keep_pollling(self):
        return self.is_verfication_still_valid() and self.is_verification_still_pending()

    def wait_for_verification(self):
        while self.should_keep_pollling():
            sleep(self.__verification_poll_interval)
            self.try_fetch_token()

    def get_token(self):
        if self.__token_res:
            return self.__token_res.get('access_token')
        else:
            return None

    def get_parsed_id_token(self):
        if self.__token_res:
            id_token = self.__token_res.get('id_token')
            return jwt.decode(id_token, verify=False)
        else:
            return None