# Routes

# login

```
{
    "Content-Type: application/json"
}

POST: {uri}/auth

{
    "username":"myusername",
    "password":"mypassword"
}
```

# user

```
{
    "Authorization: JWT <access_token>"
    "Content-Type: application/json"
}
POST: {uri}/api/v1/user
```

# registro

```

{
    "Content-Type: application/json"
}

POST: {uri}/api/v1/register

{
    "username":"myusername",
    "password":"mypassword"
}
```

# preguntas

```
{
    "Content-Type: application/json"
}

GET: {uri}/api/v1/questions
```

# Obtener puntuacion

```
{
    "Authorization: JWT <access_token>"
    "Content-Type: application/json"
}

GET {uri}/api/v1/puntuation
```

# Guardar puntuacion

```
{
    "Authorization: JWT <access_token>"
    "Content-Type: application/json"
}

POST {uri}/api/v1/puntuation

{
    "puntuacion":"0",
    "tiempo":"00:00:00"
}
```
