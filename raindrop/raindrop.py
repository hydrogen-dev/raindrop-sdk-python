import httplib2, json, secrets

# Define a function
def health():
    print("Hello, World!")

def verify(username, password, user, message, application_id):
    h = httplib2.Http(".cache")
    h.add_credentials(username, password)
    resp, content = h.request("https://dev.hydrogenplatform.com/hydro/v1/verify_signature?username="+user+"&msg="+message+"&application_id="+application_id,
        "GET",
        headers={'content-type':'application/json'} )

    resp_json = json.loads(content.decode("utf-8"))
    return(resp_json["verified"])

def addClientToApp(username, password, user, application_id):
    h = httplib2.Http(".cache")
    h.add_credentials(username, password)
    resp, content = h.request("https://dev.hydrogenplatform.com/hydro/v1/application/client?username="+user+"&application_id="+application_id,
        "POST",
        headers={'content-type':'application/json'} )

    resp_json = json.loads(content.decode("utf-8"))
    return(resp_json["application_client_mapping_id"])

def generateMessage():
    code = str(secrets.randbelow(int(1e6))).zfill(6)
    return(code)
