import models
import new_app as app

from flask_migrate import Migrate

application = app.app
migrate = Migrate(application, app.db)
