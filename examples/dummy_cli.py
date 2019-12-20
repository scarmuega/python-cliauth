from time import sleep
from cliauth import DeviceAuthFlow, DeviceAuthConfig

config = DeviceAuthConfig(
    device_authorization_url="<provider>/oauth/device/code",
    oauth_token_url="<provider>/oauth/token",
    client_id="<client id>",
    scope="profile openid",
    audience="<audience>"
)

flow = DeviceAuthFlow(config)
flow.start()

print("open the following link in your browser to finish authorization")
print(flow.get_verification_uri_complete())

flow.wait_for_verification()

token = flow.get_token()

if token:
    print("login successful")
    print(flow.get_parsed_id_token())
else:
    print("unable to authorize")