from flask import render_template,Flask,jsonify,request
from flask_pymongo import PyMongo
from bson.json_util import dumps,RELAXED_JSON_OPTIONS
import json 
import random
import string
import datetime
from bson.objectid import ObjectId
from flask_mail import Mail, Message
from flask_cors import CORS, cross_origin
app = Flask(__name__)
mail= Mail(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# mail setting
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'bobwatcherx@gmail.com'
app.config['MAIL_PASSWORD'] = 'amigos2010'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


app.config["MONGO_URI"] = "mongodb+srv://bobwatcherx:amigos2010@cluster0.wta9g.mongodb.net/test?retryWrites=true&w=majority"
mongo = PyMongo(app)

@app.route("/",methods=['GET'])
@cross_origin()
def index():
	docs_list  = mongo.db.datanew.find()
	resp = dumps(docs_list)
	return resp


@app.route("/search",methods=['GET'])
@cross_origin()
def search():
	kota = request.args.get('kota')
	cekin = request.args.get('cekin')
	cekout = request.args.get('cekout')
	mytype = request.args.get('type')
	data = mongo.db.datanew.find({
		"lokasi" : kota,
		"type":mytype
		})
	return dumps(data)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))	

@app.route("/addnewbook",methods=['POST'])
@cross_origin()
def newPost():
	nama = request.form.get('nama')
	hotel = request.form.get('hotel')
	harga = request.form.get('harga')
	cekin = request.form.get('cekin')
	cekout = request.form.get('cekout')
	totalguest = request.form.get('totalguest')
	kodebook = id_generator()
	totalroom = request.form.get('totalroom')
	datenow = datetime.datetime.now()
	oldidhotel = request.form.get('oldidhotel')
	email = request.form.get('email')


	if request.method == "POST" and nama and email and harga and hotel and cekin and cekout and  totalguest and totalroom  and oldidhotel:
		try:
			req = mongo.db.datacustbook.insert({
			"nama":nama,
			"jumlahorang":totalguest,
			"hotel":hotel,
			"harga":harga,
			"kodebook":kodebook,
			"dateorder":datenow,
			"idhotel":oldidhotel,
			"totalroom":totalroom,
			"cekin":cekin,
			"cekout":cekout,
			"email":email
			})
			return jsonify({"kodebook":kodebook})
		except Exception as e:
			return  jsonify({"error":"error"})


	return jsonify({
		"message":"data success add"
		})

@app.route("/update/<id>",methods=["PUT"])
@cross_origin()
def update(id):
		getdata = mongo.db.datanew.find({"_id":ObjectId(id)},{"available":1})
		for e in getdata:
			available =  e['available']

		newdata = int(available) - int(request.form.get('totalroom'))
		updatedata = mongo.db.datanew.update({
			"_id":ObjectId(id)},{"$set":{"available":newdata}}
			)

		return jsonify({
			"message":"udh ke update"
			})

@app.route("/removebook/<id>",methods=["DELETE"])
@cross_origin()
def delete(id):
	deleteitem = mongo.db.datacustbook.remove({"_id":ObjectId(id)})
	return jsonify({
		"message":"data booking terhapus " 
		})



if __name__ == '__main__':
   app.run(debug = True)	