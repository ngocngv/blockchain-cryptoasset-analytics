from flask_migrate import MigrateCommand
from flask_script import Manager

from application import create_app
from application.commands import InitDbCommand

import config

manager = Manager(create_app)
manager.add_option("-c", "--config", dest="config", required=True)
manager.add_command('db', MigrateCommand)
manager.add_command('init_db', InitDbCommand)

if __name__ == "__main__":
    manager.run()