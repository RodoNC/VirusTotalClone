How to run: Firstly you will need two terminal/commandline in order to run this program. One is for the Python Backend while the other is for the Javascript Frontend

**ALSO PLEASE NOTE PYTHON BACKEND RUNS ON : http://127.0.0.1:5000/ If yours is different please go into /teamD/frontend/src/setupProxy.js and change the LINE 7: target: 'http://127.0.0.1:5000/', into your python backend ip.**

Steps on how to run this program.

Python Terminal|

inside of the directory /teamD/backend | run your pip install here.

Python Dependency or check requirements.txt:
**pip install -r requirements.txt**

**python3 server.py** <= this will boot up your backend.

Now we will open up a new terminal to run our frontend.

JavaScript Terminal|

inside of the directory /teamD/frontend. \
**cd frontend** <= to get into javascript code. \
**npm install** <= Install Javascript (react) Dependency. \
**npm start** <= this will boot up the frontend and open up a webpage for you usually at http://localhost:3000/.
