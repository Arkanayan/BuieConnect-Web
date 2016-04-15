# BuieConnect-Web
This the backend cloud code for BuieConnect app


## Urls
- Base url: **__/api/v1/__**
- User operation urls
    - **_user_** : 
        - Request methods allowed **GET**, **PUT**
        - Require **Auth token**
        - Returns 
            - **GET**: get details of the current user identified by the token
            - **PUT**: modifies the current user identified by the token
        - Example:
        ```javascript
        {
          "gcm_reg_id": "gcm registration id",
          "current_semester": 2,
          "lastName": "Last Name",
          "email": "email@mail.com",
          "admission_year": 2000,
          "is_admin": true,
          "reg_date": "2016-04-06T11:35:51.146837+00:00",
          "google_sub": "34234234234",
          "is_alumnus": false,
          "url": "http://<site_url>/api/v1/users/1",
          "univ_roll": 2013,
          "passout_year": 2016,
          "firstName": "First Name",
          "department_name": "CSE",
          "verified": false,
          "id": 1
        }
        ```