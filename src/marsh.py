from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from domain import Region, City, Company



class CompanySchema(ModelSchema):
  class Meta:
    model = Company



class CitySchema(ModelSchema):
  companies = fields.Method('getCompanies')
  class Meta:
    model = City

  def getCompanies(self, region):
    if "with" in self.context and "companies" in self.context["with"]:
      return companiesSchema.dump(region.companies).data
    return []



class RegionSchema(ModelSchema):
  cities = fields.Method('getCities')
  class Meta:
    model = Region

  def getCities(self, region):
    if "with" in self.context and "cities" in self.context["with"]:
      return citiesSchema.dump(region.cities).data
    return []



regionSchema = RegionSchema()
regionsSchema = RegionSchema(many = True)

citySchema = CitySchema()
citiesSchema = CitySchema(many = True)

companySchema = CompanySchema()
companiesSchema = CompanySchema(many = True)