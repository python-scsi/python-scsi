class Enum(type):
    ''' A class for  pseudo enumerators '''

    def __new__(cls,*args, **kwargs):
        if len(args) > 0:
            if len(args) == 1:
                if type(args[0]).__name__ == 'dict':
                    tmp = args[0]
                else:
                    tmp ={}
            else:
                tmp = dict()
        elif len(kwargs) > 0:
            if len(kwargs) == 1:
                tmp = kwargs
            else:
                tmp = dict(**kwargs)
        else:
            tmp = dict()
        tmp['_enums'] = tmp.keys()
        return type.__new__(cls, cls.__name__, (), tmp)

    def __init__(self,*args,**kwargs):
        print self._enums
        setattr(self,'add',classmethod(self.__class__.add))
        setattr(self,'remove',classmethod(self.__class__.remove))

    def add(self,key,value):
        if not key in self._enums:
            self._enums.append(key)
            setattr(self,key,value)


    def remove(self,key):
        if key in self._enums:
            delattr(self,key)
            self._enums.remove(key)
