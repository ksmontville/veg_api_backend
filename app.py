from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['JSON_SORT_KEYS'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
cors = CORS(app, origins=['https://chop-that-veg.netlify.app/',
                          'http://localhost:5173',
                          'http://localhost:5174',
                          'http://localhost:5175'],
            allow_headers=['*'])


welcome_msg = "Welcome to the Chop That Veg API!"


@app.route('/')
def welcome():
    return welcome_msg, 200


@app.get('/veggies/')
def show_veg():
    veggies = Vegetable.query.order_by(Vegetable.name)
    return [vegetable_schema.dump(veg) for veg in veggies], 200


@app.get('/veggies/<int:veg_id>/')
def get_veg_by_id(veg_id):
    """Get a specific produce by its id (primary key)"""
    veg = Vegetable.query.get_or_404(veg_id, "Sorry, item not currently in database! Consider adding it with a POST request.")
    return vegetable_schema.dump(veg), 200


@app.get('/veggies/<name>')
def get_veg_by_name(name):
    """Get a specific produce by its id (primary key)"""
    veg = Vegetable.query.filter(Vegetable.name == name).first()
    return vegetable_schema.dump(veg), 200


@app.post('/veggies/')
def add_vegetable():
    data = request.get_json()

    new_veg = Vegetable(
        name=data['name'],
        description=data['description'],
        resource=data['resource'],
        procedure=data['procedure']
    )

    db.session.add(new_veg)
    db.session.commit()

    return vegetable_schema.dump(new_veg), 201


@app.put('/veggies/<name>/')
def edit_vegetable(name):
    data = request.get_json()

    veg = Vegetable.query.filter(Vegetable.name == name).first()

    veg.name = data['name']
    veg.description = data['description']
    veg.resource = data['resource']
    veg.procedure = data['procedure']

    db.session.commit()

    return vegetable_schema.dump(veg), 201


@app.delete('/veggies/<name>/')
def delete_vegetable_by_name(name):
    data = request.get_json()

    veg = Vegetable.query.filter(Vegetable.name == name).first()
    db.session.delete(veg)
    db.session.commit()

    return "Item deleted successfully."


@app.delete('/veggies/<int:veg_id>/')
def delete_vegetable_by_id(veg_id):
    data = request.get_json()

    veg = Vegetable.query.filter(Vegetable.id == veg_id).first()
    db.session.delete(veg)
    db.session.commit()

    return "Item deleted successfully."


# Define a database model
class Vegetable(db.Model):
    """A class for managing vegetable entries in the API."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(100), nullable=True)
    resource = db.Column(db.String(100), nullable=True)
    procedure = db.Column(db.String(), nullable=True)

    def __repr__(self):
        """Return a string representation of the model."""
        return self.name


# Define a model schema
class VegetableSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Vegetable

    id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()
    resource = ma.auto_field()
    procedure = ma.auto_field()


vegetable_schema = VegetableSchema()

