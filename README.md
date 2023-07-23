## Running instructions
setup virtual environment
```commandline
python3 -m venv venv
. venv/bin/activate
```

Install dependencies
```commandline
pip install -r requirements.txt
```

Run flask server: this command will start up the server at port 5000
```commandline
flask run -p 5000
```

### Create User cURL
```
curl --location --request POST 'localhost:5000/create/user' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "achint3",
    "passcode": "asdasda"
}'
```

### Response
```
{
    "status": "success"
}
```

### Login cURL
```
curl --location --request POST 'localhost:5000/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "achint1",
    "passcode": "ThisIsATestPassWord"
}'
```
### Response:
```
{
    "status": "success",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2OTAwNzUzMDR9.fT5eOQ6LacjKglHMJYwEZbeRAGYllEbSnsAXLWS8hpE"
}
```

### get all users cURL
```
curl --location --request GET 'localhost:5000/get/users' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "achint5",
    "passcode": "asdasda"
}'
```

### Response
```
{
    "data": [
        "achint1",
        "achint2",
        "achint3"
    ],
    "status": "success"
}
```

### send text to a user: you need to pass the Auth token in header that you received during login
```
curl --location --request POST 'localhost:5000/send/text/user' \
--header 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2OTAwNzQ4NDF9.uRgcBVdJFoh952eiO2dYd_ygw2ZXGAsAwBuYN1IALnw' \
--header 'Content-Type: application/json' \
--data-raw '{
    "tousername": "achint3",
    "text": "achint 1, message 3"
}'
```

### Response
```
{
    "status": "success"
}
```

### get unread messages, you need to pass the auth token you received during login
```
curl --location --request GET 'localhost:5000/get/unread' \
--header 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2OTAwNzQ5Mzh9.TL86ZU1IimkhRh2XlEGfw_hrbABsupt0kSFtrAHt1kQ'
```

### Response
```
{
    "data": [
        {
            "texts": [
                "group message by achint 1asdasd",
                "group message by achint 1asdasd",
                "achint 1, message 1",
                "achint 1, message 2",
                "achint 1, message 2"
            ],
            "username": "achint1"
        },
        {
            "texts": [
                "achint 2, message 1",
                "achint 2, message 2"
            ],
            "username": "achint2"
        }
    ],
    "message": "You have 7 new messages",
    "status": "success"
}
```

### get history 
```
curl --location --request GET 'localhost:5000/get/history?fromusername=achint1' \
--header 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2OTAwNzUzMDR9.fT5eOQ6LacjKglHMJYwEZbeRAGYllEbSnsAXLWS8hpE' \
--header 'Content-Type: application/json' \
--data-raw '{
    "tousername": "achint6",
    "text": "Hello achint, testing 2"
}'
```

### Response
```
{
    "status": "success",
    "texts": [
        "achint 1, message 1",
        "achint 1, message 2",
        "achint 1, message 3",
        "achint 1, message 3",
        "group message by achint 1"
    ]
}
```

### logout
```
curl --location --request POST 'localhost:5000/logout' \
--header 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2OTAwNzQ5Mzh9.TL86ZU1IimkhRh2XlEGfw_hrbABsupt0kSFtrAHt1kQ' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "achint1",
    "passcode": "asdasda"
}'
```

### Response
```
{
    "status": "success"
}
```

### group messages
```
curl --location --request POST 'localhost:5000/send/text/group' \
--header 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2OTAwNzQ4NDF9.uRgcBVdJFoh952eiO2dYd_ygw2ZXGAsAwBuYN1IALnw' \
--header 'Content-Type: application/json' \
--data-raw '{
    "tousernames": ["achint3", "achint2"],
    "text": "group message by achint 1asdasd"
}'
```


### Response
```
{
    "message": "Group message sent successfully.",
    "status": "success"
}
```