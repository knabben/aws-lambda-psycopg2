# aws-lambda-psycopg2

A custom lambda authenticator for API Gateway

Building Lambda psycopg2
---

```
$ make build_pgsql
```

Psycopg2 depency is on psycopg2/ folder

Now you must create the zip file for it:

```
$ make build_zip
```

Creating the function
--

You must create your function first on Lambda with the following command:

```
aws lambda create-function --region us-east-1 --function-name authenticator --zip-file \
    fileb://code.zip --handler auth.handler --runtime python3.6 --role $(roleARN)
```

Setting environment variables to access the database:


Updating func code
---

To update the code in the function, after building a new zip file:

```
$ make update_code
```
