'''littlesis - a python wrapper for the littlesis.org api'''
import json,urllib2,gzip
from StringIO import StringIO

class LittleSis(object):
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

  def relationship(self,id):
    return Relationship(id,self.key)

  def list(self,id):
    return List(id,self.key)

class LittleSisObject(LittleSis):
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
  type="Entity"

  @property
  def details(self):
    return self.request("/details.json")["Response"]["Data"]["Entity"]

  @property
  def aliases(self):
    return self.request("/aliases.json")["Response"]["Data"]["Entity"]["Aliases"]["Alias"]

  @property
  def relationships(self):
    return [Relationship(int(i["id"]),self.key) for i in self.request("/relationships.json")["Response"]["Data"]["Relationships"]["Relationship"]]

  @property
  def related(self):  
    return [Entity(int(i["id"]),self.key) for i in
    self.request("/related.json")["Response"]["Data"]["RelatedEntities"]["Entity"]]
  
  def __repr__(self):
    return u"LittleSis Entity: %d (%s)"%(self.id,self.name)

  def __str__(self):
    return self.name


class Relationship(LittleSisObject):
  type="Relationship"
  
  @property
  def entity1(self):
    return Entity(int(self.Entity1["id"]),self.key,data=self.Entity1)
  
  @property
  def entity2(self):
    return Entity(int(self.Entity2["id"]),self.key,data=self.Entity2)

  def __repr__(self):
    return u"LittleSis Relationship: %d (%s - %s - %s)"%(self.id,
      self.Entity1["name"],self.description1,self.Entity2["name"])
    
class List(LittleSisObject):
  type="List"
