from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from requests import post
import os

IMG_FOLDER = os.path.join('avatars')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Data.db'
app.config['UPLOAD_FOLDER'] = IMG_FOLDER
db = SQLAlchemy(app)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    status = db.Column(db.String)
    species = db.Column(db.String)
    Type = db.Column(db.String)
    gender = db.Column(db.String)
    created = db.Column(db.String)


@app.route('/', methods=['POST', 'GET'])
def index():
    items = Data.query.order_by(Data.id).all()
    return render_template('index.html', data = items)


@app.route('/Create', methods=['POST', 'GET'])
def Create():
    if request.method == "POST":
        item = Data()
        item.name = request.form['name']
        item.status = request.form['status']
        item.species = request.form['species']
        item.Type = request.form['Type']
        item.gender = request.form['gender']
        db.session.add(item)
        try:
            db.session.commit()
            return redirect('/')
        except:
            return redirect('/Create')
    img = os.path.join(app.config['UPLOAD_FOLDER'] + '/' + '-1' + '.jpeg')
    return render_template('Create.html', img=img)


@app.route('/Edit/<int:item_id>', methods=['POST', 'GET'])
def Edit(item_id):
    if request.method == "POST":
        item = db.session.get(Data, item_id)
        item.name = request.form['name']
        item.status = request.form['status']
        item.species = request.form['species']
        item.Type = request.form['Type']
        item.gender = request.form['gender']
        try:
            db.session.commit()
            return redirect('/')
        except:
            print(item.email, item.nickname, item.password)
            return redirect('/Edit/'+item_id)
    item = db.session.get(Data, item_id)
    img = os.path.join(app.config['UPLOAD_FOLDER'] + '/' + str(item_id) + '.jpeg')
    return render_template('Edit.html', data = item, img=img)

@app.route('/Character/<int:item_id>', methods=['POST', 'GET'])
def Character(item_id):
    if request.method == "POST":
        delete = db.session.get(Data, item_id)
        print(delete)
        db.session.delete(delete)
        db.session.commit()
        try:
            os.remove('./static/avatars/'+str(item_id))
        except:
            return redirect('/')
        return redirect('/')

    item = db.session.get(Data, item_id)
    img = os.path.join(app.config['UPLOAD_FOLDER'] + '/' + str(item_id) + '.jpeg')
    if os.path.exists('./static/'+img) == False:
        img = '/avatars/-1.jpeg'
    return render_template('Character.html', data = item, img = img)

if __name__ == "__main__":
    app.run(debug=False)
