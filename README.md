## 1. First create dummy account to test the project demo, 
because the current dummy account is mostly loggedin from Indonesia proxy it is may be blocked if use in other region.

## 2. Input account username and password in docker-selenium-lambda/linked_account.json

- Get cookie
    1. on directory demo-serverless
    2. RUN python docker-selenium-lambda/get_cookie.py --> this to get login cookie

- Deploy
    1. npm install -g serverless --> if you dont have serverless installed
    2. cd docker-selenium-lambda
    3. serverless deploy

