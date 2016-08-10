from flask import Flask, abort, flash, make_response, redirect, render_template, request, session, url_for, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import StringField, IntegerField, DateField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    birth_date = db.Column(db.Date)
    zip_code = db.Column(db.Integer)

    def __init__(self, first_name, last_name, birth_date, zip_code):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.zip_code = zip_code

    def __repr__(self):
        return '<Name: {} {}, Birth Date: {}, Zip Code: {}>'\
            .format(self.first_name, self.last_name, self.birth_date, self.zip_code)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class PersonForm(Form):
    firstName = StringField('firstName', validators=[DataRequired()])
    lastName = StringField('lastName', validators=[DataRequired()])
    birthDate = DateField('birthDate', format='%Y-%m-%d', validators=[DataRequired()])
    zipCode = StringField('zipCode', validators=[DataRequired()])


@app.route('/')
def main():
    return send_file('static/index.html')


@app.route('/person/', methods=['GET'])
def index():
    offset = request.args.get('offset')
    if offset:
        persons_list = Person.query.offset(offset).limit(50).all()
    else:
        persons_list = Person.query.all()
    return jsonify({'persons': [person.as_dict() for person in persons_list]})


@app.route('/person/<person_id>', methods=['GET'])
def show(person_id):
    person_to_show = Person.query.get_or_404(person_id)
    print(person_to_show)
    return jsonify({'persons': [person_to_show.as_dict()]})


@app.route('/person/', methods=['POST'])
def create():
    form = PersonForm(csrf_enabled=False)
    if not form.validate_on_submit():
        return make_response('Bad Request.', 400)
    person_to_create = Person(form.firstName.data, form.lastName.data, form.birthDate.data, form.zipCode.data)
    db.session.add(person_to_create)
    db.session.commit()
    return jsonify(person_to_create.as_dict())


@app.route('/person/<int:person_id>', methods=['PUT'])
def update(person_id):
    form = PersonForm(csrf_enabled=False)
    if not form.validate_on_submit():
        return make_response('Bad Request.', 400)
    person_to_update = Person.query.get_or_404(person_id)

    person_to_update.first_name = form.firstName.data
    person_to_update.last_name = form.lastName.data
    person_to_update.birth_date = form.birthDate.data
    person_to_update.zip_code = form.zipCode.data

    db.session.add(person_to_update)
    db.session.commit()
    return jsonify(person_to_update.as_dict())


@app.route('/person/<person_id>', methods=['DELETE'])
def delete(person_id):
    person_to_delete = Person.query.get_or_404(person_id)
    db.session.delete(person_to_delete)
    db.session.commit()
    return jsonify({'status': 204, 'message': 'No Content.'})

if __name__ == '__main__':
    app.run()
