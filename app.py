from flask import Flask

app = Flask(__name__)  #set up app


#create index route
@app.route('/')  #paste url of our app
def index():
    return "Hello world"


if __name__ == "__main__":
    app.run(debug=True)

