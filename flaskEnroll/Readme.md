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
