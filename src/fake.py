from domain import Region, City, Company
from app import app, db

app.app_context().push()

regions = {
  "Свердловская область": {
    "Первоуральcк": {
      "Даниловское": "http://localhost:8080",
      "Альфа": "http://localhost:8070"
    },
    "Ревда": {}
  },
  "Челябинская область": {
    "Челябинск": {
      "Челябинское": ""
    }
  }
}

for regionName, cities in regions.items():
  region = Region(regionName)
  db.session.add(region)
  for cityName, companies in cities.items():
    city = City(region, cityName)
    db.session.add(city)
    for companyName, url in companies.items():
      company = Company(companyName, url)
      city.companies.append(company)
      db.session.add(company)

db.session.commit()
