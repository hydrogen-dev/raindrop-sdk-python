# Hydro Raindrop
This package provides a suite of convenience functions intended to simplify the integration of Hydro's [Raindrop authentication](https://www.hydrogenplatform.com/hydro) into your project. An equivalent [Python SDK](https://github.com/hydrogen-dev/raindrop-sdk-python) is also available. More information, including detailed API documentation, is available in the [Raindrop documentation](https://www.hydrogenplatform.com/docs/hydro/v1/#Raindrop). Raindrop comes in two flavors:

## Client-side Raindrop
Client-side Raindrop is a next-gen 2FA solution. We've open-sourced the [code powering Client-side Raindrop](https://github.com/hydrogen-dev/smart-contracts/tree/master/raindrop-client).


## Server-side Raindrop
Server-side Raindrop is an enterprise-level security protocol to secure APIs and other shared resources. We've open-sourced the [code powering Server-side Raindrop](https://github.com/hydrogen-dev/smart-contracts/tree/master/hydro-token-and-raindrop-enterprise).


## Installation
### Recommended
Install [raindrop on pypi](https://pypi.org/project/raindrop/). Supports Python >=3.6.
```
pip install raindrop
```

## Getting started
The `raindrop` package defines two classes that you will interact with: `ServerRaindropPartner` and `ClientRaindropPartner`. To start making API calls, you'll need to instantiate a each object. The SDK will automatically fetch you an [OAuth token](https://www.hydrogenplatform.com/docs/hydro/v1/#Authentication), and set [your environment](https://www.hydrogenplatform.com/docs/hydro/v1/#Environment).

## `ClientRaindropPartner` Functions
```python
ClientRaindropPartner('Sandbox', 'your_id', 'your_secret', 'your_application_id')
```
- `environment` (required): `Sandbox` | `Production` to set your environment
- `client_id` (required): Your OAuth id for the Hydro API
- `client_secret` (required): Your OAuth secret for the Hydro API
- `application_id` (required): Your application id for the Hydro API

### `register_user(username)`
Should be called when a user elects to use Raindrop Client for the first time with your application.
- `username`: the new user's Hydro username (the one they used when signing up for Hydro mobile app)

### `verify_signature(username, message)`
Should be called each time you need to verify whether a user has signed a message.
- `username`: the username of the user that is meant to have signed `message`
- `message`: a message generated from `generate_message()` (or any 6-digit numeric code)

### `unregister_user(username)`
Should be called when a user disables Client-side Raindrop with your application.
- `username`: the user's Hydro username (the one they used when signing up for Hydro mobile app)

### `generate_message()`
Generates a random 6-digit integers for users to sign. Uses system-level CSPRNG.


## `ServerRaindropPartner` Functions
```python
ServerRaindropPartner('Sandbox', 'your_id', 'your_secret')
```
- `environment` (required): `Sandbox` | `Production` to set your environment
- `client_id` (required): Your OAuth id for the Hydro API
- `client_secret` (required): Your OAuth secret for the Hydro API

### `whitelist(address)`
A one-time call that whitelists a user to authenticate with your API via Server-side Raindrop.
- `address`: The Ethereum address of the user you're whitelisting

### `request_challenge(hydro_address_id)`
Initiate an authentication attempt on behalf of the user associated with `hydro_address_id`.
- `hydro_address_id`: the `hydro_address_id` of the authenticating user

### `authenticate(hydro_address_id)`
Checks whether the user correctly performed the raindrop.
- `hydro_address_id`: the `hydro_address_id` of the user who claims to be authenticated


## Generic Functions
### `refresh_token()`
Manually refreshes OAuth token.

### `transactionStatus(transaction_hash)`
This function returns true when the transaction referenced by `transaction_hash` has been included in a block on the Ethereum blockchain (Rinkeby if the environment is `Sandbox`, Mainnet if the environment is `Production`).
- `transaction_hash` (required): Hash of a transaction

## `Note:`
Many of the above functions have optional parameters `raise_for_status` and `return_json`. These parameters turn status code error handling and json return values on/off. They are set to sensible defaut parameters.


## Copyright & License
Copyright 2018 The Hydrogen Technology Corporation under the GNU General Public License v3.0.
