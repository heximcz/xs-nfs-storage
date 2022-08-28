class XSException(Exception):
    """ Basic class for exceptions """
    pass

class ConfigException(XSException):
    """ Config class for exceptions """
    pass

class MySQLException(XSException):
    """ MySQL class for exceptions """
    pass

class XenAPIException(XSException):
    """ XenAPI class for exceptions """
    pass
