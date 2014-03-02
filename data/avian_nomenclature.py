#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2014 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 01 March 2014 08:43 PST (-0800)
"""

import csv
import pdb
import pandas as pd
import argparse
from numpy import nan

from sqlalchemy import create_engine, Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def get_args():
    """Get arguments from CLI"""
    parser = argparse.ArgumentParser(
        description="""Program description"""
    )
    parser.add_argument(
        "masterlist",
        help="""Help text"""
    )
    parser.add_argument(
        "--flag",
        action="store_true",
        default=False,
        help="""Help text""",
    )
    return parser.parse_args()

Base = declarative_base()
class Orders(Base):
    __tablename__ = 'orders'
    ord = Column(String, primary_key=True)
    code = Column(String)
    comment = Column(String)

    def __init__(self, ord, code, comment):
        self.ord = ord
        self.code = code
        self.comment = comment

    def __repr__(self):
        return "<Orders('{}')>".format(self.ord)


class Families(Base):
    __tablename__ = 'families'
    scientific = Column(String, primary_key=True)
    english = Column(String, index=True)
    code = Column(String)
    comment = Column(String)

    def __init__(self, scientific, english, code, comment):
        self.scientific = scientific
        self.english = english
        self.code = code
        self.comment = comment

    def __repr__(self):
        return "<Families('{} {}')>".format(self.scientific, self.english)

class Genera(Base):
    __tablename__ = 'genera'
    genus = Column(String, primary_key=True)
    authority = Column(String)
    code = Column(String)
    comment = Column(String)

    def __init__(self, genus, authority, code, comment):
        self.genus = genus
        self.authority = authority
        self.code = code
        self.comment = comment

    def __repr__(self):
        return "<Genera('{}')>".format(self.genus)

class Species(Base):
    __tablename__ = 'species'
    id = Column(Integer, Sequence('species_id_seq'), primary_key=True)
    ord = Column(String, ForeignKey("orders.ord"), nullable=False, index=True)
    family = Column(String, ForeignKey("families.scientific"), nullable=False, index=True)
    genus =  Column(String, ForeignKey("genera.genus"), nullable=False, index=True)
    species = Column(String, index=True)
    authority = Column(String)
    common = Column(String, index=True)
    breed_region = Column(String)
    breed_subregion = Column(String)
    nonbreed = Column(String)
    code = Column(String)
    comment = Column(String)
    binomial = Column(String, unique=True, index=True)

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

class Subspecies(Base):
    __tablename__ = 'subspecies'
    id = Column(Integer, Sequence('species_id_seq'), primary_key=True)
    ord = Column(String, ForeignKey("orders.ord"), nullable=False, index=True)
    family = Column(String, ForeignKey("families.scientific"), nullable=False, index=True)
    genus =  Column(String, ForeignKey("genera.genus"), nullable=False, index=True)
    species = Column(String, index=True)
    subspecies = Column(String, index=True)
    authority = Column(String)
    common = Column(String)
    breed_region = Column(String)
    breed_subregion = Column(String)
    nonbreed = Column(String)
    code = Column(String)
    comment = Column(String)
    trinomial = Column(String, unique=True, index=True)

    def __init__(self, order, family, genus, species, subspecies, authority, common, breed_region, breed_subregion, nonbreed, code, comment, trinomial):
        self.ord = order
        self.family = family
        self.genus = genus
        self.species = species
        self.subspecies = species
        self.authority = authority
        self.common = common
        self.breed_region = breed_region
        self.breed_subregion = breed_subregion
        self.nonbreed = nonbreed
        self.code = code
        self.comment = comment
        self.trinomial = trinomial

    def __repr__(self):
        return "<Subspecies('{}')>".format(self.trinomial)


def prep_and_insert_order(session, order):
    all_order_data = [Orders(o['Order'], o['Code'], o['Comment']) for _, o in order.iterrows()]
    session.add_all(all_order_data)

def prep_and_insert_family(session, family):
    all_family_data = [Families(f['Family (Scientific)'], f['Family (English)'], f['Code'], f['Comment']) for _, f in family.iterrows()]
    session.add_all(all_family_data)

def prep_and_insert_genus(session, genus):
    all_genus_data = [Genera(g['Genus'], g['Authority'], g['Code'], g['Comment']) for _, g in genus.iterrows()]
    session.add_all(all_genus_data)

def prep_and_insert_species(session, species):
    all_species_data = [Species(
        s['Order'],
        s['Family (Scientific)'],
        s['Genus'],
        s['Species (Scientific)'],
        s['Authority'],
        s['Species (English)'],
        s['Breeding Range-Region'],
        s['Breeding Range-Subregion(s)'],
        s['Nonbreeding Range'],
        s['Code'],
        s['Comment'],
        s['Binomial'])
        for _, s in species.iterrows()]
    session.add_all(all_species_data)

def prep_and_insert_subspecies(session, subspecies):
    all_subspecies_data = [Subspecies(
        s['Order'],
        s['Family (Scientific)'],
        s['Genus'],
        s['Species (Scientific)'],
        s['Subspecies'],
        s['Authority'],
        s['Species (English)'],
        s['Breeding Range-Region'],
        s['Breeding Range-Subregion(s)'],
        s['Nonbreeding Range'],
        s['Code'],
        s['Comment'],
        s['Trinomial'])
        for _, s in subspecies.iterrows()]
    session.add_all(all_subspecies_data)

def enter_data_to_db(order, family, genus, species, subspecies):
    engine = create_engine('sqlite:///birds.sqlite', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    prep_and_insert_order(session, order)
    prep_and_insert_family(session, family)
    prep_and_insert_genus(session, genus)
    prep_and_insert_species(session, species)
    prep_and_insert_subspecies(session, subspecies)
    #pdb.set_trace()
    session.commit()


def main():
    args = get_args()
    orderl = []
    familyl = []
    genusl = []
    speciesl = []
    subspeciesl = []
    xl = pd.read_excel(args.masterlist, "Master", index_col=None, na_values=['NA'])
    #pdb.set_trace()
    for index, row in xl.iterrows():
        if row['Order'] is not nan and row[1:4].all() is nan:
            orderl.append(row)
            curr_order = row['Order']
        elif row['Family (Scientific)'] is not nan and row['Order'] is nan:
            familyl.append(row)
            curr_family_sci = row['Family (Scientific)']
            curr_family_comm = row['Family (English)']
        elif row['Genus'] is not nan and row[0:3].all() is nan:
            genusl.append(row)
            curr_genus = row['Genus']
        elif row['Species (Scientific)'] is not nan and row[0:4].all() is nan:
            row['Order'] = curr_order
            row['Family (Scientific)'] = curr_family_sci
            row['Family (English)'] = curr_family_comm
            row['Genus'] = curr_genus
            new_row = row.set_value("Binomial", u"{} {}".format(
                row['Genus'],
                row['Species (Scientific)']
                )
            )
            speciesl.append(new_row)
            curr_species = row['Species (Scientific)']
        elif row['Subspecies'] is not nan and row[0:5].all() is nan:
            row['Order'] = curr_order
            row['Family (Scientific)'] = curr_family_sci
            row['Family (English)'] = curr_family_comm
            row['Genus'] = curr_genus
            row['Species (Scientific)'] = curr_species
            new_row = row.set_value("Trinomial", u"{} {} {}".format(
                row['Genus'],
                row['Species (Scientific)'],
                row['Subspecies']
                )
            )
            subspeciesl.append(new_row)
    # convert series to data frames
    order = pd.DataFrame(orderl)
    family = pd.DataFrame(familyl)
    genus = pd.DataFrame(genusl)
    species = pd.DataFrame(speciesl)
    subspecies = pd.DataFrame(subspeciesl)
    # setup output files
    output_files = {
        "order.txt": [order, ['Order', 'Code', 'Comment']],
        "family.txt": [family, ['Family (Scientific)', 'Family (English)', 'Code', 'Comment']],
        "genus.txt": [genus, ['Genus', 'Authority', 'Code', 'Comment']],
        "species.txt": [species, None],
        "subspecies.txt": [subspecies, None]
    }
    # create output files
    for name, values in output_files.iteritems():
        df, cols = values
        df.to_csv(name, sep="\t", na_rep=".", cols=cols, index=False, encoding="UTF-8", quoting=csv.QUOTE_ALL)
    # database
    enter_data_to_db(order, family, genus, species, subspecies)
    #pdb.set_trace()



if __name__ == '__main__':
    main()
