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
  """ The base LittleSis Object"""
  def __init__(self,key):
    self.key=key
    self.api="http://api.littlesis.org/"

  def request(self,path,params=None):
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
    return Entity(id,self.key)

  def entities(self,q):
    """entity search"""
    r=self.request("/entities.json",{"q":q})["Response"]["Data"]["Entities"]["Entity"]
    if type(r)!=list:
      r=[r]
    return [Entity(int(i["id"]),self.key,data=i) for i in r]

  def relationship(self,id):
    return Relationship(id,self.key)

  def list(self,id):
    return List(id,self.key)

class LittleSisObject(LittleSis):
  """ A instance of a Little Sis object (has an ID) """
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
  """ An Entity Object """
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
