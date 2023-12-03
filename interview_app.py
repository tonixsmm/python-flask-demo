import pickle

# we are going to use the Flask micro web framework for our prediction web app
# Goal: Create a web app or a simple/predict API service
from flask import Flask, request, jsonify

app = Flask(__name__)

def load_model():
    # unpickle tree.p
    infile = open("tree.p", "rb")
    header, tree = pickle.load(infile)
    infile.close()
    return header, tree

def tdidt_predict(header, tree, instance):
    info_type = tree[0]
    if info_type == "Leaf":
        return tree[1] # label
    att_index = header.index(tree[1])
    for i in range(2, len(tree)):
        value_list = tree[i]
        if value_list[1] == instance[att_index]:
            return tdidt_predict(header, value_list[2], instance)

# we need to add routes
# a "route" is a function that handles a request
# e.g. a webpage or for an API response, etc.
# lets add a route for the home AKA index page
# also called the index route
@app.route("/")
def index():
    # return content and status code
    return "<h1>Welcome to my app!!</h1>", 200

# lets make a route for the /predict endpoint
@app.route("/predict")
def predict():
    # we need to parse the query string to get info for the unseen instance
    level = request.args.get("level") # returns None if invalid key
    lang = request.args.get("lang")
    tweets = request.args.get("tweets")
    phd = request.args.get("phd")
    # make a prediction!
    header, tree = load_model()
    pred = tdidt_predict(header, tree, [level, lang, tweets, phd])
    if pred is not None:
        return jsonify({"prediction": pred}), 200
    return "Error making prediction", 400 # bad request
    

if __name__ == "__main__":
    # header, tree = load_model()
    # print(header)
    # print(tree)
    app.run(debug=True, port=5001)
    # TODO: set debug=False when deploy
    # default port number is 5000; however, if running in a docker container
    # you need to check port forwarding