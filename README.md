# Hydro Raindrop
This package provides a suite of convenience functions intended to simplify the integration of Hydro's [Raindrop authentication](https://www.hydrogenplatform.com/hydro) into your project. An equivalent [Javascript SDK](https://github.com/hydrogen-dev/raindrop-sdk-js) is also available. Raindrop is available in two flavors:

## Raindrop Enterprise
Raindrop Enterprise is an enterprise-level security protocol to secure APIs. The open-source code powering Raindrop enterprise is available [here](https://github.com/hydrogen-dev/smart-contracts/tree/master/hydro-token-and-raindrop-enterprise). For more information, please refer to the [Raindrop Enterprise documentation](https://www.hydrogenplatform.com/docs/hydro/v1/#Raindrop).

## Raindrop Client
Raindrop Client is an innovative next-gen 2FA solution. The open-source code powering Raindrop enterprise is available [here](https://github.com/hydrogen-dev/smart-contracts/tree/master/raindrop-client).

## Installation
### Recommended
Install [raindrop on pypi](https://pypi.org/project/raindrop/):
```
pip install raindrop
```

## Getting started
The `raindrop` package has two main function sets: `enterprise` and `client`. Before being able to use `raindrop`, you must set your desired environment: `raindrop.setEnvironment('Sandbox'|'Production')` (see the [docs](https://www.hydrogenplatform.com/docs/hydro/v1/#Testnet) for more information).

## `enterprise` Functions
### `setEnvironment`
### `whitelist`
### `challenge`
### `authenticate`

## `client` Functions
### `generateMessage`
### `addClientToApp`
### `verify`

## Copyright & License
Copyright 2018 The Hydrogen Technology Corporation under the GNU General Public License v3.0.
