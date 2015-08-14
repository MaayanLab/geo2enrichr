# This is only for development.
#
# In production, Flask is run by mod_wsgi, which imports the via wsgi.py.


from g2e import app, db

from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

manager.run()