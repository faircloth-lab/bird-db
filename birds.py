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


class Genera(db.Model):
    __tablename__ = 'genera'
    genus = db.Column(db.String, primary_key=True)
    authority = db.Column(db.String)
    code = db.Column(db.String)
    comment = db.Column(db.String)

    def __init__(self, genus, authority, code, comment):
        self.genus = genus
        self.authority = authority
        self.code = code
        self.comment = comment

    def __repr__(self):
        return "<Genera('{}')>".format(self.genus)


class Species(db.Model):
    __tablename__ = 'species'
    id = db.Column(db.Integer, db.Sequence('species_id_seq'), primary_key=True)
    ord = db.Column(db.String, db.ForeignKey("orders.ord"), nullable=False, index=True)
    family = db.Column(db.String, db.ForeignKey("families.scientific"), nullable=False, index=True)
    genus =  db.Column(db.String, db.ForeignKey("genera.genus"), nullable=False, index=True)
    species = db.Column(db.String, index=True)
    authority = db.Column(db.String)
    common = db.Column(db.String, index=True)
    breed_region = db.Column(db.String)
    breed_subregion = db.Column(db.String)
    nonbreed = db.Column(db.String)
    code = db.Column(db.String)
    comment = db.Column(db.String)
    binomial = db.Column(db.String, unique=True, index=True)

    def __init__(self, order, family, genus, species, authority, common, breed_region, breed_subregion, nonbreed, code, comment, binomial):
        self.ord = order
        self.family = family
        self.genus = genus
        self.species = species
        self.authority = authority
        self.common = common
        self.breed_region = breed_region
        self.breed_subregion = breed_subregion
        self.nonbreed = nonbreed
        self.code = code
        self.comment = comment
        self.binomial = binomial

    def __repr__(self):
        return "<Species('{}')>".format(self.binomial)


def citation_info():
    return {
        'website': 'IOC World Bird List v4.1',
        'url': 'http://www.worldbirdnames.org/',
        'doi': '10.14344/IOC.ML.4.1',
        'citation': 'Gill, F & D Donsker (Eds). 2014. IOC World Bird List (v 4.1). doi: 10.14344/IOC.ML.4.1'
    }

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

    return jsonify(attribution=citation_info(), records=json_results)


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

    return jsonify(attribution=citation_info(), records=json_results)


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

    return jsonify(attribution=citation_info(), records=json_results)


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

    return jsonify(attribution=citation_info(), records=json_results)


@app.route('/family/common/<string:common_name>', methods=['GET'])
def family_common(common_name):
  if request.method == 'GET':
    results = Families.query.filter(Families.english.like("{}%".format(common_name))).all()
    json_results = []
    for result in results:
        d = {
            'scientific': result.scientific,
            'common': result.english,
            'code': result.code,
            'comment': result.comment
        }
        json_results.append(d)

    return jsonify(attribution=citation_info(), records=json_results)


@app.route('/genus/', methods=['GET'])
def genera():
  if request.method == 'GET':
    results = Genera.query.limit(100).offset(0).all()
    json_results = []
    for result in results:
        d = {
            'genus': result.genus,
            'authority': result.authority,
            'code': result.code,
            'comment': result.comment
        }
        json_results.append(d)

    return jsonify(attribution=citation_info(), records=json_results)


@app.route('/genus/<string:name>', methods=['GET'])
def genus_common(name):
  if request.method == 'GET':
    results = Genera.query.filter(Genera.genus.like("{}%".format(name))).all()
    json_results = []
    for result in results:
        d = {
            'genus': result.genus,
            'authority': result.authority,
            'code': result.code,
            'comment': result.comment
        }
        json_results.append(d)

    return jsonify(attribution=citation_info(), records=json_results)


@app.route('/species/', methods=['GET'])
def species():
  if request.method == 'GET':
    results = Species.query.limit(100).offset(0).all()
    json_results = []
    for result in results:
        d = {
            'order': result.ord,
            'family': result.family,
            'genus': result.genus,
            'species': result.species,
            'authority': result.authority,
            'common': result.common,
            'breed_region': result.breed_region,
            'breed_subregion': result.breed_subregion,
            'nonbreed': result.nonbreed,
            'code': result.code,
            'comment': result.comment,
            'binomial': result.binomial
        }
        json_results.append(d)

    return jsonify(attribution=citation_info(), records=json_results)


@app.route('/species/common/<string:common_name>', methods=['GET'])
def species_common(common_name):
  if request.method == 'GET':
    results = Species.query.filter(Species.common.like("{}%".format(common_name))).all()
    json_results = []
    for result in results:
        d = {
            'order': result.ord,
            'family': result.family,
            'genus': result.genus,
            'species': result.species,
            'authority': result.authority,
            'common': result.common,
            'breed_region': result.breed_region,
            'breed_subregion': result.breed_subregion,
            'nonbreed': result.nonbreed,
            'code': result.code,
            'comment': result.comment,
            'binomial': result.binomial
        }
        json_results.append(d)

    return jsonify(attribution=citation_info(), records=json_results)




if __name__ == '__main__':
    app.run(debug=True)
