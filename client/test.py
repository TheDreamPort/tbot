import requests

u = "https://127.0.0.1/api/v1/reading"
token = "a7a8a56e95e1be87bfa646ae095b249328f29652eb2510d9b972b6fec8837181"
d = {'appliance':2, 'data':{'1':1}}
r = requests.post( u, json=d, verify=False )
print( r.content )