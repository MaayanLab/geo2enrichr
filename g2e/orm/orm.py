from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker

from orm.commondb import Base, engine
import orm.models as ms


Session = sessionmaker()
Session.configure(bind=engine)

# Do this need to run every time?
Base.metadata.create_all(engine)


@contextmanager
def session_scope():
    """Provides a transactional scope around a series of operations. Credit:
    http://docs.sqlalchemy.org/en/rel_0_9/orm/session_basics.html.
    """
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()


def save_soft_file(name, is_geo=False):
    with session_scope() as session:
        softfile = ms.SoftFile(name, is_geo)
        return softfile.id



if __name__ == '__main__':
    pass
    #genelist = GeneList()
    #extraction = Extraction()
    #extraction.genelist = genelist
    #session.add(genelist)
    #session.add(extraction)
    #session.commit()

