from flask import Blueprint, Response, request, current_app
from flask.json import dumps
from requests import post
from marsh import regionsSchema, regionSchema, citySchema, companySchema
from domain import db, Region, City, Company, Session



def getResponseSchema(Schema, itemsOrItem):
  response = Schema.dump(itemsOrItem).data
  return Response(dumps(response),  mimetype = "application/json")



app = Blueprint('PublicApi', __name__)



# Получение всех областей
@app.route("/region/")
def getRegions():
  regions = Region.query.order_by(Region.name.asc()).all()
  return getResponseSchema(regionsSchema, regions)



# Получение области по regionId
@app.route("/region/<int:regionId>")
def getRegion(regionId):
  region = Region.query.get(regionId)
  regionSchema.context = {"with": request.args.get("with", "").split(",")}
  return getResponseSchema(regionSchema, region)



# Получение города по cityId
@app.route("/city/<int:cityId>")
def getCity(cityId):
  city = City.query.get(cityId)
  citySchema.context = {"with": request.args.get("with", "").split(",")}
  return getResponseSchema(citySchema, city)



# Получение компании по companyId
@app.route("/company/<int:companyId>")
def getCompany(companyId):
  current_app.logger.info("Выбрана компания companyId = {0}".format(companyId))
  company = Company.query.get(companyId)
  return getResponseSchema(companySchema, company)



# Авторизация лицевого счета
@app.route("/authRequest/", methods = ["post"])
def createAuthRequest():
  args = request.get_json()
  company = Company.query.get(args["companyId"])
  if company:
    res = post(company.url + "/auth/", params = args, timeout = (2,2))
    if res.status_code == 200:
      json = res.json()
      req = Session(company, json["id"])
      db.session.add(req)
      db.session.commit()
      args["uid"] = req.id
      args["number"] = json
      current_app.logger.info("Авторизовался login = {0}, companyId = {1}".format(args["login"], company.id))
    elif res.status_code == 401:
      current_app.logger.warning("Не смог авторизоваться login = {0}, companyId = {1}".format(args["login"], company.id))
      args["error"] = "unauthorized"
    else:
      current_app.logger.warning("Проблемы с api company = {0}, url = {1}".format(company.id, company.url))
      args["error"] = "api_problem"
  else:
    current_app.logger.warning("Нет компании c companyId = {0}".format(args["companyId"]))
    args["error"] = "not_found_company"
  return Response(dumps(args),  mimetype = "application/json")