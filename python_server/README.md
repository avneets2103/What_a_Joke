Flask Backend template for use 
## How to Start using:
#### 1. Clone the repo:
`git clone https://github.com/avneetsingh/Flask-template.git`
#### 2. Open the cloned repo:
`cd Flask-template`
#### 3. Start a virtual environment:
`python -m venv venv`
```
for windows:
.\venv\Scripts\activate

for macos:
source venv/bin/activate
```
#### 4. Create a .env file:
`touch .env`
#### 5. Add the following variables to the .env file:
```
PORT = 4000
```
#### 6. Install dependencies:
`python install -r requirement.txt`

#### 7. Run the server:
`python main.py`   

## Included packages: 
blinker==1.8.2
boto3==1.35.33
botocore==1.35.33
click==8.1.7
dnspython==2.6.1
Flask==3.0.3
Flask-Cors==5.0.0
Flask-PyMongo==2.3.0
itsdangerous==2.2.0
Jinja2==3.1.4
jmespath==1.0.1
MarkupSafe==2.1.5
pymongo==4.10.1
python-dateutil==2.9.0.post0
python-dotenv==1.0.1
s3transfer==0.10.2
six==1.16.0
urllib3==2.2.3
Werkzeug==3.0.4

## Directory Structure: 
```
root
├── src
│   ├── controllers
│   │   ├── user_controller.py  # A template controller
|  
│   ├── DB
│   │   ├── __init__.py  # DB connection with Mongo DB
|
│   ├── routes
│   │   ├── user_routes.py  # Routes for User
│   
│   ├── Utils
|   |   ├── s3.py  # AWS S3 for file storage
│   
│   ├── app.py  # Express app
│   
│   ├── constants.py  # Constants
|
|   ├── main.py  # Main file
│
├── .env                         # Environment variables
├── .gitignore                   # Ignored files and directories
├── requirements.txt             # Project metadata and dependencies
├── README.md                    # Documentation
```

