from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://greg:euclid@master:3306/euclid?charset=utf8'


engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True, echo=True)


# We should only use one instance of this class in a commonly imported module (this one).
Base = declarative_base()
