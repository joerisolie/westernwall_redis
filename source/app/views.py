import pickle
import random
import os

from app import app,forms
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from .forms import MessageForm

class Message(object):
	name = ""
	message = ""
	rating = 0
	voters = 0

	def __init__(self, name, message,rating,voters):
		self.message = message
		self.name = name
		self.rating = rating
		self.voters = voters


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET','POST'])
def index():
	form = MessageForm()

	if form.validate_on_submit():
		flash("User %s posted message %s" % (form.name.data, form.message.data))		
		m = Message(form.name.data,form.message.data,3,0)
		pickledObj = pickle.dumps(m)
		loc = random.randint(0,35)
		#app.redis.lpush('messages', pickledObj)	
		app.redis.lset('messages', loc, pickledObj)
		app.redis.ltrim('messages', 0, 35)
	
	qry = app.redis.lrange('messages', 0, -1)

	messages = []
	for q in qry:
		messages.append(pickle.loads(q))

	return render_template('index.html', title='The Western Wall', messages=messages, form=form)

@app.route('/dbinit', methods=['GET','POST'])
def dbinit():
	app.redis.flushall()
	count = 0
	while count < 36:
		m = Message("", "", 3, 0)
		pickledObj = pickle.dumps(m)
		app.redis.lpush('messages', pickledObj)
		count += 1
	return "DB initiated"

@app.route('/ipcheck')
def ipcheck():
	retvalue = os.popen("ip addr show").readlines()
	yourip = request.remote_addr
	return render_template('ipcheck.html', title='The Western Wall - IP Check', ipinfos = retvalue, yourip=yourip)
