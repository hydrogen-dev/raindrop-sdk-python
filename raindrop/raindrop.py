import secrets
import requests

from requests.auth import HTTPBasicAuth


class BasicPartner(object):
    acceptable_environments = {
        'Dev': 'https://dev.hydrogenplatform.com',
        'QA': 'https://qa.hydrogenplatform.com',
        'Sandbox': 'https://sandbox.hydrogenplatform.com',
        'Production': 'https://api.hydrogenplatform.com'
    }

    def __init__(self, environment, client_id, client_secret):
        self.environment = None
        self.url = None
        self.token = None
        self.client_id = client_id
        self.client_secret = client_secret

        self.set_environment(environment)
        self.refresh_token()

    def set_environment(self, environment):
        assert environment in self.acceptable_environments.keys(),\
            f"Environment must be one of: {' | '.join(self.acceptable_environments.keys())}."
        self.environment = environment
        self.api_url = self.acceptable_environments[self.environment]

    def refresh_token(self):
        url = f'{self.api_url}/authorization/v1/oauth/token'
        r = requests.post(
            url, params={'grant_type': 'client_credentials'}, auth=HTTPBasicAuth(self.client_id, self.client_secret)
        )
        r.raise_for_status()
        self.OAuth_token = r.json()['access_token']

    def call_hydro_API(self, verb, endpoint, query_string_parameters=None, return_json=False, raise_for_status=True):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.OAuth_token}'
        }
        url = f'{self.api_url}/hydro/v1{endpoint}'
        r = requests.request(verb, url=url, params=query_string_parameters, headers=headers)

        if raise_for_status:
            r.raise_for_status()
        if return_json:
            assert raise_for_status, "Cannot return a JSON without checking for status"
            return r.json()
        else:
            return r

    def verify_transaction(self, transaction_hash):
        return self.call_hydro_API('GET', '/transaction', {'transaction_hash': transaction_hash})


class ServerRaindropPartner(BasicPartner):
    def whitelist(self, address, return_json=True, raise_for_status=True):
        return self.call_hydro_API(
            'POST', f'/whitelist/{address}', return_json=return_json, raise_for_status=raise_for_status
        )

    def request_challenge(self, hydro_address_id, return_json=True, raise_for_status=True):
        return self.call_hydro_API(
            'POST',
            '/challenge',
            {'hydro_address_id': hydro_address_id},
            return_json=return_json,
            raise_for_status=raise_for_status
        )

    def authenticate(self, hydro_address_id, return_json=True, raise_for_status=True):
        return self.call_hydro_API(
            'GET',
            '/authenticate',
            {'hydro_address_id': hydro_address_id},
            return_json=return_json,
            raise_for_status=raise_for_status
        )


class ClientRaindropPartner(BasicPartner):
    def __init__(self, environment, client_id, client_secret, application_id):
        self.application_id = application_id
        super(ClientRaindropPartner, self).__init__(environment, client_id, client_secret)

    def verify_signature(self, username, message, return_json=True, raise_for_status=True):
        return self.call_hydro_API(
            'GET',
            '/verify_signature',
            {'username': username, 'msg': message, 'application_id': self.application_id},
            return_json=return_json,
            raise_for_status=raise_for_status
        )

    def register_user(self, username):
        return self.call_hydro_API(
            'POST',
            '/application/client',
            {'username': username, 'application_id': self.application_id},
            return_json=False,
            raise_for_status=True
        )

    def unregister_user(self, username):
        return self.call_hydro_API(
            'DELETE',
            '/application/client',
            {'username': username, 'application_id': self.application_id},
            return_json=False,
            raise_for_status=True
        )

    @staticmethod
    def generate_message():
        return str(secrets.randbelow(int(1e6))).zfill(6)
