
from flask import Flask, jsonify, request

from model.song import Song, SongSchema

from db.db_create import create_table
from db.db_select import  get_songs


#INITIAL SETUP
#create_table()
song_list = get_songs();

app = Flask(__name__)


@app.route('/songs',methods=['GET'])
def getAllSongs():
    return jsonify({"songs": e.serialize() for e in song_list})


@app.route('/songs/<songId>',methods=['GET'])
def getEmp(songId):
    print(songId)
    print(song_list[0].song_id)
    song = [y for y in song_list if y.song_id == int(songId)][0]

    return jsonify(song.serialize())



@app.route('/songs/<songId>',methods=['PUT'])
def updateEmp(songId):
    em = [ song for song in song_list if (song.song_id == songId) ]
    if 'name' in request.json : 
        em[0]['name'] = request.json['name']
    if 'title' in request.json:
        em[0]['title'] = request.json['title']
    return jsonify({'emp':em[0]})


@app.route('/songs',methods=['POST'])
def createEmp():
    dat = {
    'title':request.json['title'],
    'author':request.json['author'],
    'created':request.json['created'],
    'updated':request.json['updated']
    }
    empDB.append(dat)
    return jsonify(dat)


@app.route('/songs/<songId>',methods=['DELETE'])
def deleteEmp(songId):
    em = [ emp for emp in song_list if (emp['id'] == songId) ]
    if len(em) == 0:
       abort(404)
    song_list.remove(em[0])
    return jsonify({'response':'Success'})



if __name__ == '__main__':
    app.run()