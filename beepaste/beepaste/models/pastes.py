import datetime # will be used to set default dates on models
from .meta import Base # we need to import our sqlalchemy metadata from which model classes will inherit
from sqlalchemy import (
    Column,
    Integer,
    Unicode,     # will provide Unicode field
    UnicodeText, # will provide Unicode text field
    DateTime,    # time abstraction field
    Boolean,     # for expiration check
)

class Pastes(Base):
    __tablename__ = 'pastes'
    id = Column(Integer, primary_key=True)
    pasteURI = Column(Unicode(6), unique=True,nullable=False)
    title = Column(Unicode(255), default=u'Untitled')
    name = Column(Unicode(255), default=u'Anonymous')
    username = Column(Unicode(255), nullable=True)
    lang = Column(Unicode(15), default=u'text')
    text = Column(UnicodeText, nullable=False)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    expire = Column(DateTime, default=datetime.datetime.utcnow)
    toexpire = Column(Boolean, default=False)
    shortURL = Column(Unicode(25), default=u'')
    encryption = Column(Unicode(6), default=u'no')
