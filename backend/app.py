from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS
from datetime import timedelta

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://carford_user:carford_password@db:5432/carford_db"
)
app.config["JWT_SECRET_KEY"] = "super-secret-key"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)


class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    opportunity = db.Column(db.Boolean, default=True)
    vehicles = db.relationship("Vehicle", backref="owner", lazy=True)


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(
        db.Enum("yellow", "blue", "gray", name="car_color"), nullable=False
    )
    model = db.Column(
        db.Enum("hatch", "sedan", "convertible", name="car_model"),
        nullable=False
    )
    owner_id = db.Column(db.Integer, db.ForeignKey("owner.id"), nullable=False)


@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/owner", methods=["POST"])
@jwt_required()
def create_owner():
    data = request.get_json()
    new_owner = Owner(name=data["name"],
                      opportunity=data.get("opportunity", True))
    db.session.add(new_owner)
    db.session.commit()
    ownerName = data['name']
    return jsonify({
        "message":
        f"Proprietário criado com sucesso! {ownerName}"
    }), 201


@app.route("/owner/<int:owner_id>/vehicle", methods=["POST"])
@jwt_required()
def add_vehicle(owner_id):
    owner = Owner.query.get_or_404(owner_id)
    if len(owner.vehicles) >= 3:
        return (
            jsonify(
                {
                    "message":
                    "O proprietário já tem o número máximo de veículos"
                }),
            400,
        )
    data = request.get_json()
    new_vehicle = Vehicle(color=data["color"],
                          model=data["model"], owner_id=owner_id)
    db.session.add(new_vehicle)
    db.session.commit()
    return jsonify({"message": "Veículo adicionado com sucesso!"}), 201


@app.route('/owners', methods=['GET'])
@jwt_required()
def list_owners():
    owners = Owner.query.all()
    owner_list = []
    for owner in owners:
        vehicles = [{'color': v.color, 'model': v.model}
                    for v in owner.vehicles]
        owner_list.append({
            'id': owner.id,
            'name': owner.name,
            'opportunity': owner.opportunity,
            'vehicles': vehicles
        })
    return jsonify(owner_list), 200


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    # password = request.json.get("password")
    # TODO: user validation
    access_token = create_access_token(
        identity=username, expires_delta=timedelta(hours=1)
    )
    return jsonify(access_token=access_token)


if __name__ == '__main__':
    app.run()
