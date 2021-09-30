from ..models import Song,SongSchema
from flask import jsonify, request
from . import main
from app import db

@main.route("/songs",methods = ['GET'])
def get_all_songs():
	songs = Song.get_all()

	serializer = SongSchema(many=True)

	data = serializer.dump(songs)

	return jsonify(data)


@main.route("/songs",methods = ['POST'])
def create_a_song():
	data = request.get_json()
	new_song = Song(title = data.get('title'),artist = data.get('artist'), urlToCover = data.get('urlToCover'))
	new_song.save()
	serializer = SongSchema()
	data = serializer.dump(new_song)
	return jsonify(data),201

@main.route("/song/<int:id>",methods = ['GET'])
def get_song(id):

	song = Song.get_by_id(id)
	serializer = SongSchema()
	data = serializer.dump(song)
	return jsonify(data),200


@main.route("/song/<int:id>",methods = ['PUT'])
def update_song(id):
	song_to_update = Song.get_by_id(id)
	data = request.get_json()
	song_to_update.title = data.get('title')
	song_to_update.artist = data.get('artist')
	song_to_update.urlToCover = data.get('urlToCover')

	db.session.commit()
	serializer = SongSchema()
	song_data = serializer.dump(song_to_update)
	return jsonify(song_data),200


@main.route("/song/<int:id>",methods = ['PUT'])
def delete_song(id):
	song_to_delete = Song.get_by_id(id)
	song_to_delete.delete()
	return jsonify({'message':'deleted'}),204

@main.errorhandler(500)
def internal_server(error):
	return jsonify({'message':'There was a problem'}),500

@main.errorhandler(404)
def not_found(error):
	return jsonify({'message':'Resource not found'}),404
