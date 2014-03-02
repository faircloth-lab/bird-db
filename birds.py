from flask import Flask, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/birds.sqlite'


class Orders(db.Model):
    __tablename__ = 'orders'
    ord = db.Column(db.String, primary_key=True)
    code = db.Column(db.String)
    comment = db.Column(db.String)

    def __init__(self, ord, code, comment):
        self.ord = ord
        self.code = code
        self.comment = comment

    def __repr__(self):
        return "<Orders('{}')>".format(self.ord)


class Families(db.Model):
    __tablename__ = 'families'
    scientific = db.Column(db.String, primary_key=True)
    english = db.Column(db.String, index=True)
    code = db.Column(db.String)
    comment = db.Column(db.String)

    def __init__(self, scientific, english, code, comment):
        self.scientific = scientific
        self.english = english
        self.code = code
        self.comment = comment

    def __repr__(self):
        return "<Families('{} {}')>".format(self.scientific, self.english)


@app.route('/order/', methods=['GET'])
def orders():
  if request.method == 'GET':
    results = Orders.query.limit(100).offset(0).all()
    json_results = []
    for result in results:
        d = {
            'order': result.ord,
            'code': result.code,
            'comment': result.comment
        }
        json_results.append(d)

    return jsonify(items=json_results)


@app.route('/order/<string:order_name>', methods=['GET'])
def order(order_name):
  if request.method == 'GET':
    results = Orders.query.filter(Orders.ord.like("{}%".format(order_name))).all()
    json_results = []

    for result in results:
        d = {
            'order': result.ord,
            'code': result.code,
            'comment': result.comment
        }
        json_results.append(d)

    return jsonify(items=json_results)


@app.route('/family/', methods=['GET'])
def families():
  if request.method == 'GET':
    results = Families.query.limit(100).offset(0).all()
    json_results = []
    for result in results:
        d = {
            'scientific': result.scientific,
            'common': result.english,
            'code': result.code,
            'comment': result.comment
        }
        json_results.append(d)

    return jsonify(items=json_results)


@app.route('/family/scientific/<string:scientific_name>', methods=['GET'])
def family_scientific(scientific_name):
  if request.method == 'GET':
    results = Families.query.filter(Families.scientific.like("{}%".format(scientific_name))).all()
    json_results = []
    for result in results:
        d = {
            'scientific': result.scientific,
            'common': result.english,
            'code': result.code,
            'comment': result.comment
        }
        json_results.append(d)

    return jsonify(items=json_results)


@app.route('/family/common/<string:common_name>', methods=['GET'])
def family_common(common_name):
  if request.method == 'GET':
    results = Families.query.filter(Families.common.like("{}%".format(common_name))).all()
    json_results = []
    for result in results:
        d = {
            'scientific': result.scientific,
            'common': result.english,
            'code': result.code,
            'comment': result.comment
        }
        json_results.append(d)

    return jsonify(items=json_results)


if __name__ == '__main__':
    app.run(debug=True)
