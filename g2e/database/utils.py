"""Utility methods for interacting with the database.
"""

from contextlib import contextmanager

from substrate import db as substrate_db


@contextmanager
def session_scope():
    """Provides a transactional scope around a series of operations. Credit:
    http://docs.sqlalchemy.org/en/rel_0_9/orm/session_basics.html.
    """
    try:
        yield substrate_db.session
        substrate_db.session.commit()
    except Exception as e:
        print('Rolling back database')
        print(e)
        substrate_db.session.rollback()


def get_or_create(model, **kwargs):
    _kwargs = {
        k: v.decode('utf-8') if isinstance(v, bytes) else v
        for k, v in kwargs.items()
    }
    instance = substrate_db.session.query(model).filter_by(**_kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**_kwargs)
        substrate_db.session.add(instance)
        substrate_db.session.commit()
        return instance
