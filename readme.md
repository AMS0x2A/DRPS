
## DRPS (Distributed Rock Paper Scissors)

This project was originally built in Java as a client/server application to play rock paper scissors over a distributed system. Since then, it has been migrated to Python Flask. As a web server, clients make an account then can play rock paper scissors against other accounts or a robot. Their history and queue is recorded and viewable. Passwords are hashed on form submit then encrypted with bcrypt. The Flask app is wrapped with ProxyFix and Gunicorn. MongoDB is the database used.


### Setup

For anyone forking this repository, there are a few steps necessary for setup. A configuration file must be created that holds the application's initialization variables like a secret key, uri for MongoDB connectivity, etc.

In the root directory, create a file named ```.env``` in the project's directory.
The MongoDB cluster should have at least one database with at least one collection. The collection must be named ```Accounts```. The collection must have one document that has the key ```usernames``` and the value of an empty array.

#### .env

This file requires the following keys: ```SECRET_KEY, MONGO_URI, DATABASE_NAME, HOST, USERNAMES_ID```. These values must be initialized for the application to work.

| Key | Value Info |
|--|--|
| SECRET_KEY | The secret key for the application; should be randomly generated
| MONGO_URI | The uri for connecting to the MongoDB cluster
| DATABASE_NAME | The name of the database in the MongoDB cluster
| HOST | The host ip address; either localhost or 0.0.0.0
| USERNAMES_ID | The ```_id``` value of the document containing ```usernames``` array

---
### Run
The application is most easily run by utilizing the project's Makefile. There are two targets within the Makefile.

|Command | Result |
|--|--|
| `make debug` | Run the application through flask debug on port 14642 |
| `make run` | Run the application through Gunicorn on port 14642 |
| `make docker` | Build and run the application in a Docker container (container port 14642; host port 14642) |

### Access
Access the application by visiting the address in a web browser.
  
---
## License
- Author is `KeVeon 'AMS0x2A' White`
- This repository uses the [MIT License](/LICENSE).
