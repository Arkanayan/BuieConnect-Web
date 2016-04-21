# BuieConnect-Web
This the backend cloud code for BuieConnect app

## Deploy requirements
- **Environment variables:**
    - _DATABASE_URI_ = \<Sqlalchemy format database uri\>
    - _GCM_API_KEY_ = \<Google Cloud Messaging api key\>
    - _CLIENT_ID_ = \<Google OAuth client id to get details of users\>
    - _SECRET_KEY_ = \<Key used to encrypt tokens\>
    - _FIREBASE_SECRET_ = \<Firebase app secret\>

## Urls
- Base url: **__/api/v1__**
- User operation urls
    - **_"/user"_** : 
        - Request methods allowed **GET**, **PUT**
        - Require headers: **Auth token**
        - Returns 
            - **GET**: get details of the current user identified by the **token**
            - **PUT**: modifies the current user identified by the **token**
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
        

    - **_"/users/\<id\>"_** : 
        - Request methods allowed **GET**, **PUT**
        - Require headers: **Auth token** of admin or the user
        - Returns 
            - **GET**: without **id**, returns array of users
            - **GET**: with **id**, get details of the current user identified by **id**
            - **PUT**: modifies the user identified by **id**
        - Example:
        ```javascript
        [
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
        [
        ```   
    - **_"/notices/\<id\>"_** : 
        - Request methods allowed **GET**
        - Require headers: None
        - Returns 
            - **GET**: without **id**, returns array of notices
            - **GET**: with **id**, returns details of the notice identified by **id**
        - Example:
        ```javascript
            {
              "id": 4,
              "message": "Notice Message",
              "title": "Notice title",
              "url": "http://<site url>/api/v1/notices/4"
            }
        ```
         
## Error Format
```javascript
{
  "code": 404,
  "errors": [], // additional errors
  "message": "Error message"
}
```