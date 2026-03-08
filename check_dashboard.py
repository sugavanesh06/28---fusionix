import requests

BASE='http://127.0.0.1:8000'
login={'username':'testinterview','password':'TestPass123'}
r=requests.post(f"{BASE}/login",json=login)
print('login',r.status_code,r.text)
if r.ok:
    token=r.json().get('access_token')
    print('token',token)
    d=requests.get(f"{BASE}/dashboard",headers={'Authorization':f'Bearer {token}'})
    print('dashboard',d.status_code,d.text)
