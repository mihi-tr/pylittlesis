'''littlesis - a python wrapper for the littlesis.org api

This module wraps the littlesis API - please note that you will need a API
key for the littlesis API. 

usage::

  from littlesis import LittleSis

  ls=LittleSis("YOURKEY")
  e=ls.entity(1)
  print e.details

'''
import json,urllib2,gzip
from StringIO import StringIO

class LittleSis(object):
  """ The base LittleSis Object
  use this to establish your API key::
    
    ls=LittleSis(key)
  
  then use it to search for entities, access entities, relationships or
  lists by id::

    e=ls.entity(1)
    print e.name
    """

  def __init__(self,key):
    self.key=key
    self.api="http://api.littlesis.org/"

  def request(self,path,params=None):
    """ Send a request to the API 

    params is an optional dictionary of parameters to be passed to the API
    - please refer to the API documentation for further information of the
      parameters you might need """
    if params:
      p="&%s"%"&".join(("%s=%s"%x for x in params.items()))
    else:
      p=""
    url="%s%s?_key=%s%s"%(self.api,path,self.key,p)
    r=urllib2.Request(url,headers={"User-Agent":
      "Mozilla/5.0 (X11; Linux x86)",
      "Accept-encoding":"gzip"})
    response=urllib2.urlopen(r)
    if response.info().get('Content-Encoding') == 'gzip':
      buf=StringIO(response.read())
      f=gzip.GzipFile(fileobj=buf)
    else:
      f=response
    return json.loads(f.read())

  def entity(self,id):
    """ return an Entitiy for the given id """
    return Entity(id,self.key)

  def entities(self,q):
    """Search for entities with the given term(s) - returns a list of
    entities"""
    r=self.request("/entities.json",{"q":q})["Response"]["Data"]["Entities"]["Entity"]
    if type(r)!=list:
      r=[r]
    return [Entity(int(i["id"]),self.key,data=i) for i in r]

  def relationship(self,id):
    """ returns a Relationshio with the given id """
    return Relationship(id,self.key)

  def list(self,id):
    """ returns a list with the given id """
    return List(id,self.key)

class LittleSisObject(LittleSis):
  """ A instance of a Little Sis object (has an ID) - this is mainly used
  for common functions of Entity, List and Relationship"""
  def __init__(self,id,key,data=None):
    self.id=id
    super(LittleSisObject,self).__init__(key)
    self.api="%s/%s/%d"%(self.api,self.type.lower(),self.id)
    if not data:
      self.__dict__["attributes"]=self.request(".json")["Response"]["Data"][self.type]
    else:
      self.__dict__["attributes"]=data
  
  def __getattr__(self,name):
    return self.attributes[name]

  def __eq__(self,other):
    return (self.id==other.id & self.type==other.type)

class Entity(LittleSisObject):
  """ An Entity Object - an entity in the LittleSis database. Entities are
  either Organizations or Persons. Initialize using id and key (optionally
  you can pass in a data dictionary of the Entities attributes).
  
  However, it is recommended to bootstrap entities from the LittleSis
  object, containing your key (use entity(id) or entities("search term")).
  """
  type="Entity"

  @property
  def details(self):
    """ get the details of the entity """
    return self.request("/details.json")["Response"]["Data"]["Entity"]

  @property
  def aliases(self):  
    """ get aliases of the entity """
    return self.request("/aliases.json")["Response"]["Data"]["Entity"]["Aliases"]["Alias"]

  @property
  def relationships(self):
    """ get relationships for this entity """
    r=self.request("/relationships.json")["Response"]["Data"]["Relationships"]["Relationship"]
    if type(r)!=list:
      r=[r]
    return [Relationship(int(i["id"]),self.key) for i in r]

  @property
  def related(self):  
    """ get related entities """
    r=self.request("/related.json")["Response"]["Data"]["RelatedEntities"]["Entity"]
    if type(r)!=list:
      r=[r]
    return [Entity(int(i["id"]),self.key,data=i) for i in r]
 
  @property
  def lists(self):
    """get the lists the entity belongs to """
    r=self.request("/lists.json")["Response"]["Data"]["Lists"]["List"]
    if type(r)!=list:
      r=[r]
    return [List(int(i["id"]),self.key,data=i) for i in r]

  def __repr__(self):
    return u"LittleSis Entity: %d (%s)"%(self.id,self.name)

  def __str__(self):
    return self.name


class Relationship(LittleSisObject):
  """ A relationship Object """
  type="Relationship"
  
  @property
  def entity1(self):
    """ Get the Entity Object of Entity1"""
    return Entity(int(self.Entity1["id"]),self.key,data=self.Entity1)
  
  @property
  def entity2(self):
    """ Get the Entity Object of Entity2 """
    return Entity(int(self.Entity2["id"]),self.key,data=self.Entity2)

  def __repr__(self):
    return u"LittleSis Relationship: %d (%s - %s - %s)"%(self.id,
      self.Entity1["name"],self.description1,self.Entity2["name"])
    
class List(LittleSisObject):
  type="List"
