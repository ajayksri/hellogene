# hellogene
This project implements a simple web service and takes care of various aspect of software development: 
- Implementation of web service
- Packaging the software
- Deploying the software

# Tested Environment
- CentOS 7.9

# Building rpm
- clone the code on the machine using command - git clone git@github.com:ajayksri/hellogene.git
- go to the base directory of source code
- run command - sh build.sh
- rpm will be available in dist directory

# Deploying the service
- The process will build the code and deploy on the local machine
- clone the code on the machine using command - git clone git@github.com:ajayksri/hellogene.git
- go to the base directory of source code
- run command - sh deploy.sh

# Run the app
- from base directory of source code, run command - sh run.sh
- This will run the application

# Accessing endpoints
- Application runs on port 5000. This should be accessible from outside
- Use curl/postman to access the endpoints
- Adding a new user using curl: curl -s -d '{"name": "Vijay"}' -H "Content-Type: application/json" http://<IP>:5000/app/hello/v1/user/vijay
- Get user using curl: curl -s -X GET -H "Content-Type: application/json" http://<IP>:5000/app/hello/v1/user/vijay

