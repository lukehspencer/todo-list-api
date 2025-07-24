# Testing flask app

import requests

URL = "http://127.0.0.1:5000/" # url that Flask app runs on (default for all Flask apps)

user = {"username": "Luke", 
        "password": "Password123"}
data1 = {"title": "Buy groceries",
         "description": "Milk, eggs, and bread"}
data2 = {"title": "Pay bills",
         "description": "Pay electricity and water bills"}

# registers a new user

#response = requests.post(URL + "register", json=user)
#response.raise_for_status()
#print(response.json())

response = requests.post(URL + "login", json=user) # logs in user
print(response.json())

if response.status_code==200:
    token = response.cookies.get("access_token") # retrieves token
    headers = {"Authorization": f"Bearer {token}"} # uses token in header and passes it into each http call     
    input()
    response = requests.post(URL + "todos", json=data1, headers=headers)
    print(response.json())
    input()
    response = requests.patch(URL + "todos/1", json={"title": "Buy groceries", "description": "Soda and chips"}, headers=headers)
    print(response.json())
    input()
    response = requests.post(URL + "todos", json=data2, headers=headers)
    print(response.json())
    input()
    response = requests.get(URL + "todos", headers=headers)
    print(response.json())
    input()
    response = requests.delete(URL + "todos/1", headers=headers)
    print(response)
    input()
    response = requests.get(URL + "todos", headers=headers)
    print(response.json())
    input()
    response = requests.delete(URL + "todos", headers=headers)
    print(response)
    input()
    response = requests.get(URL + "todos", headers=headers)
    print(response.json())
