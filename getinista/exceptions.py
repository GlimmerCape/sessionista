class GetinistaException(Exception):
    """
    Base findonista exception class.

    All findonista exceptions should subclass this class.
    """

class ProfilesDirNotFound(GetinistaException):
    """
    Exception for when no firefox profiles dir are found.
    """

