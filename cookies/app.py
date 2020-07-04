from flask import Flask, render_template, request, make_response

app = Flask(__name__)

@app.route("/")
def index():

    return "Hello World!"

# @app.route("/cookie/set")
# def set_cookie():
#     resp = make_response(render_template("index.html"))
#     resp.set_cookie("username", "CodeNoSchool")
#     return resp

@app.route("/cookie/set/<string:user>/<string:value>")
def set_cookie(user, value):
    resp = make_response(render_template("index.html"))
    resp.set_cookie(user, value)
    return resp

# @app.route("/cookie/read")
# def read_cookie():
#     username = request.cookies.get("username", None)
#     if username == None:
#         return "The cookie doesn't exist."
#     return username

@app.route("/cookie/get/<string:user>")
def get_cookie(user):
    value = request.cookies.get(user, None)
    if value == None:
        return "The cookie doesn't exist."
    return value

if __name__ == "__main__":
    app.run(debug=True)
