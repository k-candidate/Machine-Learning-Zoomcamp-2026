from flask import Flask

# create the application and give it a name.
app = Flask('ping')

# decorator: it tells Flask that the function below it should handle GET requests to the /ping address.
# This address is called a route.
@app.route('/ping', methods=['GET'])
def ping():
    # returns the response body: the string PONG.
    return "PONG"


# run the development server, but only when we execute the file directly (python ping.py), 
# not when we import it from another file.
if __name__ == "__main__":
    # make the server listen on all network interfaces (not only localhost) and set the port.
    app.run(debug=True, host='0.0.0.0', port=9696)
