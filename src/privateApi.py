from flask import Blueprint, Response, current_app, abort
from flask.json import dumps
from requests import post
from domain import Session
from functools import wraps



timeout = (0.5, 1)



# Декоратор проверяет есть ли сессия в базе данных
def session_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if not "session" in kwargs:
      current_app.logger.error("Роут оформлен неверно. Нет session переменной.")
      abort(401)
    session = Session.query.get(kwargs["session"])
    if session:
      current_app.logger.info("Найдена сессия companyId = {0}, numberId = {1} для session = {2}".format(session.company.id, session.numberId, kwargs["session"]))
      kwargs["session"] = session
      return f(*args, **kwargs)
    else:
      current_app.logger.warning("Не смог найти сессию для session = {0}".format(kwargs["session"]))
      abort(401)
  return decorated



app = Blueprint('Api', __name__)



# Прокси для однотипных действий
def proxyJsonRequest(url):
  res = post(url, timeout = timeout)
  if res.status_code != 200:
    current_app.logger.warning("Не смог получить ответ по url = {0}".format(url))
    abort(500)
  return Response(dumps(res.json()),  mimetype="application/json")



# Получение лицевого счета
@app.route("/<session>/profile/")
@session_required
def getNumber(session):
  current_app.logger.info("Получение профиля companyId = {0}, numberId = {1}".format(session.company.id, session.numberId))
  return proxyJsonRequest("{0}/{1}".format(session.company.url, session.numberId))



# Получение лицевого счета с его заявками, которые он подал из личного кабинет
@app.route("/<session>/queries/")
@session_required
def getQueries(session):
  current_app.logger.info("Получение заявок companyId = {0}, numberId = {1}".format(session.company.id, session.numberId))
  return proxyJsonRequest("{0}/{1}?with=queriesForLk".format(session.company.url, session.numberId))