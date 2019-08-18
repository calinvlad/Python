from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init database
db = SQLAlchemy(app)

# init marshmallow
ma = Marshmallow(app)


# Track Class / Model
class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    image = db.Column(db.String)
    price = db.Column(db.Float)

    def __init__(self, title, image, price):
        self.title = title
        self.image = image
        self.price = price


# Track Schema
class TrackSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'image', 'price')


# Init Schema
track_schema = TrackSchema(strict=True)
tracks_schema = TrackSchema(many=True, strict=True)


# Track Something
@app.route('/track', methods=['POST'])
# Create a track
def create_track():
    title = request.json['title']
    image = request.json['image']
    price = request.json['price']
    new_track = Track(title, image, price)

    db.session.add(new_track)
    db.session.commit()

    return track_schema.jsonify(new_track)

# Get All Tracks
@app.route('/tracks', methods=['GET'])
def get_tracks():
    all_tracks = Track.query.all()
    result = tracks_schema.dump(all_tracks)
    return jsonify(result.data)

# Get Single Track
@app.route('/track/<id>', methods=['GET'])
def get_track(id):
    track = Track.query.get(id)
    return track_schema.jsonify(track)

# Update a track
@app.route('/track/<id>', methods=['PUT'])
def update_track(id):
    track = Track.query.get(id)

    title = request.json['title']
    image = request.json['image']
    price = request.json['price']

    track.title = title
    track.price = price
    track.image = image

    db.session.commit()

    return track_schema.jsonify(track)

# Delete Track
@app.route('/track/<id>', methods=['DELETE'])
def delete_track(id):
    track = Track.query.get(id)
    db.session.delete(track)
    db.session.commit()
    return track_schema.jsonify(track)

# run server
if __name__ == '__main__':
    app.run(debug=True)
