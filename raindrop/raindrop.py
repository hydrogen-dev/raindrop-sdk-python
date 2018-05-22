import secrets
import requests

from requests.auth import HTTPBasicAuth


class BasicPartner(object):
    acceptable_environments = {
        'Sandbox': 'https://sandbox.hydrogenplatform.com',
        'Production': 'https://api.hydrogenplatform.com'
    }

    def __init__(self, environment, client_id, client_secret):
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

    def call_hydro_API(self, verb, endpoint, query_string=None, body=None, raise_for_status=True, return_json=False):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.OAuth_token}'
        }
        url = f'{self.api_url}/hydro/v1{endpoint}'
        r = requests.request(verb, url=url, params=query_string, json=body, headers=headers)

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
    def whitelist(self, address, raise_for_status=True, return_json=True):
        return self.call_hydro_API(
            'POST',
            '/whitelist',
            body={'address': address},
            raise_for_status=raise_for_status,
            return_json=return_json
        )

    def request_challenge(self, hydro_address_id, raise_for_status=True, return_json=True):
        return self.call_hydro_API(
            'POST',
            '/challenge',
            body={'hydro_address_id': hydro_address_id},
            raise_for_status=raise_for_status,
            return_json=return_json
        )

    def authenticate(self, hydro_address_id, raise_for_status=True, return_json=True):
        return self.call_hydro_API(
            'GET',
            '/authenticate',
            query_string={'hydro_address_id': hydro_address_id},
            raise_for_status=raise_for_status,
            return_json=return_json
        )


class ClientRaindropPartner(BasicPartner):
    def __init__(self, environment, client_id, client_secret, application_id):
        self.application_id = application_id
        super(ClientRaindropPartner, self).__init__(environment, client_id, client_secret)

    def register_user(self, username, raise_for_status=True):
        return self.call_hydro_API(
            'POST',
            '/application/client',
            body={'username': username, 'application_id': self.application_id},
            raise_for_status=raise_for_status,
            return_json=False
        )

    def unregister_user(self, username, raise_for_status=True):
        return self.call_hydro_API(
            'DELETE',
            '/application/client',
            query_string={'username': username, 'application_id': self.application_id},
            raise_for_status=raise_for_status,
            return_json=False
        )

    def verify_signature(self, username, message, raise_for_status=True, return_json=True):
        return self.call_hydro_API(
            'GET',
            '/verify_signature',
            query_string={'username': username, 'msg': message, 'application_id': self.application_id},
            raise_for_status=raise_for_status,
            return_json=return_json
        )

    @staticmethod
    def generate_message():
        return str(secrets.randbelow(int(1e6))).zfill(6)
