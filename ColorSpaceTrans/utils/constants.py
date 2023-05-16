class Const(object):
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't change const.%s" % name)
        if not name.isupper():
            raise self.ConstCaseError('const name "%s" is not all supercase' % name)

        self.__dict__[name] = value

const = Const()
const.ILLUMINANTS = {'D50': [ 0.3457,  0.3585], 
                    'D55': [ 0.33243, 0.34744], 
                    'D60': [0.32162624, 0.337737], 
                    'D65': [ 0.3127,  0.329]}
const.CIE_E = 0.008856451679035631
const.CIE_K = 903.2962962962963
const.K_M = 683
const.KP_M = 1700

