import json

class basejson(object):
    def dumps(self):
        return json.dumps(self.__dict__)

    def addobj(self, objname, objref):
        if type(objref) is list:
            alist = []
            for item in objref:
                alist.append(item.__dict__)
            setattr(self, objname, alist)
        else:
            setattr(self, objname, objref.__dict__)        

    def loads(self, jsonstr):
        print("TODO")
        

class jsonobj(basejson):
    def __init__(self):
        self.a=1
        self.b=2

class anobja(basejson):
    def __init__(self):
        self.c=2
        self.d=3

        


j = jsonobj()
jo = anobja()


j.ab = "3"
j.addobj('jo', jo)

arr = []
arr.append(anobja())
arr.append(anobja())


j.addobj("arrays", arr)

#print (arr)
print (j)
print (j.__dict__)
print (j.dumps())