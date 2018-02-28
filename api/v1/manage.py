import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from api import db, create_app
from api.models.user import User
from api.models.business import Business
from api.models.review import Review
from api.models.category import Category
from api.models.blacklisted_tokens import BlacklistedToken

app = create_app(config_name='production')
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
