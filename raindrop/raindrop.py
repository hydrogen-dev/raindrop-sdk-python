import httplib2, json, secrets

sandbox = "https://sandbox.hydrogenplatform.com"
production = "https://api.hydrogenplatform.com"

environment = "none"
token = "none"

# Define a function
def health():
    print("Hello, World!")

def setEnvironment(setter):
    global environment
    if setter == "sandbox":
        environment = sandbox
        return environment
    elif setter == "production":
        environment = production
        return environment
    else:
        return "Please call this function with either 'sandbox' or 'production'"

def Raindrop(username, password, env):
    setEnvironment(env)

    h = httplib2.Http(".cache")
    h.add_credentials(username, password)
    resp, content = h.request(environment + "/authorization/v1/oauth/token?grant_type=client_credentials",
        "POST",
        headers={'content-type':'application/json'} )

    resp_json = json.loads(content.decode("utf-8"))
    global token
    token = resp_json["access_token"]
    return resp_json

def verify(user, message, application_id):
    global environment
    if environment == "none":
        return "Please set the environment variable"

    h = httplib2.Http(".cache")
    resp, content = h.request(environment + "/hydro/v1/verify_signature?username="+user+"&msg="+message+"&application_id="+application_id,
        "GET",
        headers={'content-type':'application/json',
                 'Authorization': 'Bearer ' + token} )

    resp_json = json.loads(content.decode("utf-8"))
    return(resp_json)

def addClientToApp(user, application_id):
    global environment
    if environment == "none":
        return "Please set the environment variable"

    h = httplib2.Http(".cache")
    resp, content = h.request(environment + "/hydro/v1/application/client?username="+user+"&application_id="+application_id,
        "POST",
        headers={'content-type':'application/json',
                 'Authorization': 'Bearer ' + token} )

    resp_json = json.loads(content.decode("utf-8"))
    return(resp_json)

def removeClientFromApp(user, application_id):
    global environment
    if environment == "none":
        return "Please set the environment variable"

    h = httplib2.Http(".cache")
    resp, content = h.request(environment + "/hydro/v1/application/client?username="+user+"&application_id="+application_id,
        "DELETE",
        headers={'content-type':'application/json',
                 'Authorization': 'Bearer ' + token} )

    resp_json = json.loads(content.decode("utf-8"))
    return(resp_json)

def generateMessage():
    code = str(secrets.randbelow(int(1e6))).zfill(6)
    return(code)

def whitelist(address):
    global environment
    if environment == "none":
        return "Please set the environment variable"

    h = httplib2.Http(".cache")
    resp, content = h.request(environment + "/hydro/v1/whitelist/"+address,
        "POST",
        headers={'content-type':'application/json',
                 'Authorization': 'Bearer ' + token} )

    resp_json = json.loads(content.decode("utf-8"))
    return(resp_json)

def challenge(hydroAddressId):
    global environment
    if environment == "none":
        return "Please set the environment variable"

    h = httplib2.Http(".cache")
    resp, content = h.request(environment + "/hydro/v1/challenge?hydro_address_id="+hydroAddressId,
        "POST",
        headers={'content-type':'application/json',
                 'Authorization': 'Bearer ' + token} )

    resp_json = json.loads(content.decode("utf-8"))
    return(resp_json)

def authenticate(hydroAddressId):
    global environment
    if environment == "none":
        return "Please set the environment variable"

    h = httplib2.Http(".cache")
    resp, content = h.request(environment + "/hydro/v1/authenticate?hydro_address_id="+hydroAddressId,
        "GET",
        headers={'content-type':'application/json',
                 'Authorization': 'Bearer ' + token} )

    resp_json = json.loads(content.decode("utf-8"))
    return(resp_json)

def verify_transaction(transactionHash):
    global environment
    if environment == "none":
        return "Please set the environment variable"

    h = httplib2.Http(".cache")
    resp, content = h.request(environment + "/hydro/v1/transaction?transaction_hash="+transactionHash,
        "GET",
        headers={'content-type':'application/json',
                 'Authorization': 'Bearer ' + token} )

    resp_json = json.loads(content.decode("utf-8"))
    return(resp_json)
