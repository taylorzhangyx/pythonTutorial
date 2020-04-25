# How to start the application

1. Make sure the following package is installed
   1. flask
   1. flask-wtf
   1. virtualenv
   1. python3
1. Run the command to start the virtual environment
   1. windows: `flaskVenv/bin/activate`
   1. macos: `source flaskVenv/bin/activate`
1. Run `flask run` to start the app


# Ideas to extend this project further
1. Check Restx swagger support to export api documentation automatically: https://flask-restx.readthedocs.io/en/latest/swagger.html#automatically-documented-models
1. Use flask-login to use cookie to maintain user session: https://flask-login.readthedocs.io/en/latest/
1. Implement https
1. Data validation and default https://flask-restx.readthedocs.io/en/latest/marshalling.html

# Reflections
1. Flask and it's plug-ins is super easy to use.
   2. The syntax is short and powerful.
   2. The packages and modules are easy to import and implemented

1. Flask is a good front-end framework for web developing
   2. Python by nature is easy to use and is to parse the data for displaying on the webpages
   2. Due to natrue of the webpages, each page is a unit of program and self-contained, so python is flexible to be used in the scope of singe webpage.
   2. The jinja and flesk-wtf is powerful to parse the html in a python way and dynamically control the webpage

1. Flask is not ideal to be used as backend to integrate with multiple services
   2. Due to the nature of python, a dynamically typed language, it's hard for the engineer to utilize the libary, the signature and expected data is hard know, unless you look at the documentation pretty carefully and test your code pretty well.
   2. If the project get evolved into too many services and many branches, once those pieces need to be integrated together, it's hard to test/ensure that the integration is correct unless you run every branch of the code. There will be more type errors and mismatch of the data models somewhere in the code.
