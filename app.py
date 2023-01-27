import json
from flask import Flask, request

app = Flask(__name__)

with open('smartphones.json', 'r') as file:
    data = json.load(file)

@app.route("/smartphones", methods=["GET"])
def smartphones():
    price = request.args.get("price")
    results = [item for item in data if item["price"] == price]
    return str(results)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')





