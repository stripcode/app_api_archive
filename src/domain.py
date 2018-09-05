from flask_sqlalchemy import SQLAlchemy
from hashlib import sha1
from time import time

db = SQLAlchemy()



City2CompanyRelationship = db.Table('city2company',
  db.Column("cityId", db.Integer, db.ForeignKey("city.id")),
  db.Column("companyId", db.Integer, db.ForeignKey("company.id"))
)



class Region(db.Model):
  __tablename__ = "region"
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(255))
  cities = db.relationship("City", lazy = "dynamic", order_by = "City.name")

  def __init__(self, name):
    self.name = name



class City(db.Model):
  __tablename__ = "city"
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(255))
  regionId = db.Column(db.Integer, db.ForeignKey('region.id'))
  region = db.relationship("Region")
  companies = db.relationship("Company", lazy = "dynamic", secondary = City2CompanyRelationship, order_by = "Company.name")

  def __init__(self, region, name):
    if not isinstance(region, Region):
      raise RuntimeError("region = {0} is not valid".format(region))
    self.name = name
    self.region = region



class Company(db.Model):
  __tablename__ = "company"
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(255))
  url = db.Column(db.String(255))

  def __init__(self, name, url):
    self.name = name
    self.url = url



class Session(db.Model):
  __tablename__ = "authRequest"
  id = db.Column(db.String(64), primary_key = True)
  numberId = db.Column(db.Integer)
  companyId = db.Column(db.Integer, db.ForeignKey('company.id'))
  company = db.relationship("Company")

  def __init__(self, company, numberId):
    if not isinstance(company, Company):
      raise RuntimeError("company = {0} is not valid".format(company))
    src = str(time()) + str(company.id)  + str(company.name) + str(numberId)
    self.id = sha1(src.encode("utf-8")).hexdigest()
    self.numberId = numberId
    self.company = company