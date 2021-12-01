from oauth2client import file, client, tools # type: ignore

def init_credentials(credentials, token, scope):
    store = file.Storage(token)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(credentials, scope)
        creds = tools.run_flow(flow, store)
    return creds
