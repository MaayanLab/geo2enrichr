"""Utility methods for interacting with the database.
"""


from contextlib import contextmanager

from g2e import db


@contextmanager
def session_scope():
    """Provides a transactional scope around a series of operations. Credit:
    http://docs.sqlalchemy.org/en/rel_0_9/orm/session_basics.html.
    """
    try:
        yield db.session
        db.session.commit()
    except Exception as e:
        print 'Rolling back database'
        print e
        db.session.rollback()


def get_or_create(model, **kwargs):
    instance = db.session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance