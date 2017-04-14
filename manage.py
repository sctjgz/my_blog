
import os

from flask_uploads import IMAGES, configure_uploads, patch_request_class
from flask_uploads import UploadSet
from app import create_app, db
from app.models import User, Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
