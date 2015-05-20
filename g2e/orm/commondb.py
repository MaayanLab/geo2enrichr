"""Manages per machine connections to the database depending on config files.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# This is a little hacky but it works. *Don't* version control db.conf.
# PURPLE_WIRE: One day, this should probably read from an XML file or
# something more semantically rich.
f = open('g2e/orm/db.conf')
SQLALCHEMY_DATABASE_URI = f.read().strip()
f.close()

engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)#, echo=True)

# We should only use one instance of this class in a commonly imported module (this one).
Base = declarative_base()

Session = sessionmaker()
Session.configure(bind=engine)
