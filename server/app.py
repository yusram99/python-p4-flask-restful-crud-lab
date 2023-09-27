#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class PlantResource(Resource):
    def get(self):
        # Implement the Index Route
        plants = Plant.query.all()
        return [plant.to_dict() for plant in plants]

    def post(self):
        # Implement the Create Route
        data = request.get_json()
        name = data.get('name')
        image = data.get('image')
        price = data.get('price')

        if not name or not image or price is None:
            return {'error': 'Missing data'}, 400

        new_plant = Plant(name=name, image=image, price=price)
        db.session.add(new_plant)
        db.session.commit()

        return new_plant.to_dict(), 201


class PlantByIDResource(Resource):
    def get(self, id):
        # Implement the Show Route
        plant = Plant.query.get(id)
        if not plant:
            return {'error': 'Plant not found'}, 404
        return plant.to_dict(), 200

    def patch(self, id):
        # Implement the Update Route
        plant = Plant.query.get(id)
        if not plant:
            return {'error': 'Plant not found'}, 404

        data = request.get_json()
        if 'is_in_stock' in data:
            plant.is_in_stock = data['is_in_stock']
            db.session.commit()

        return plant.to_dict(), 200

    def delete(self, id):
        # Implement the Delete Route
        plant = Plant.query.get(id)
        if not plant:
            return '', 204  # No Content

        db.session.delete(plant)
        db.session.commit()
        return '', 204  # No Content


# Add routes to the Flask-RESTful API
api.add_resource(PlantResource, '/plants')
api.add_resource(PlantByIDResource, '/plants/<int:id>')


if __name__ == '__main__':
    app.run(port=5552, debug=True)
