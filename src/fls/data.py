import fls


class BaseContainer(object):
    def size(self):
        return len(self)

    def dump(self, file_object, sformat=fls.JSON):
        fls.dump(self, file_object, sformat)
    
    def dumps(self, sformat=fls.JSON):
        return fls.dumps(self, sformat)


class Structure(dict, BaseContainer):
    def __getattr__(self, attribute):
        if attribute in self:
            return self[attribute]
        else:
            return getattr(super(Structure, self), attribute)

    def __setattr__(self, attribute, value):
        self[attribute] = value