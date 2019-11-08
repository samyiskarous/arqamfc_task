from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
# that Api is built on top of App
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'about': 'Hello World!'}
    def post(self):
        submitted_json_data = request.get_json();
        return {'Submitted Data': submitted_json_data}, 201

class Multi(Resource):
    def get(self, number):
        return {'result': (number * 10)}
    
api.add_resource(HelloWorld, '/')
api.add_resource(Multi, '/multi/<int:number>')

if __name__ == '__main__':
    app.run(debug=True)