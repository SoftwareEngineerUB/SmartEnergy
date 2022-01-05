from flask import Flask
from flask_migrate import Migrate

from app.meter.meter import Meter
from app.models import User
from app.models.db import db


class Database:
    @staticmethod
    def importRelevantData(app):
        # Migrate database
        migrate = Migrate(app, db)

        # Initiate database
        db.init_app(app)
        with app.app_context():
            db.create_all()
        migrate.init_app(app)

        with app.app_context():
            # Create or select user
            username = 'mock-user'
            user = db.session.query(User).filter_by(username=username).first()
            if user is None:
                user = User(username=username, email=username + '@smartenergy.cloud')
                user.set_password('password')
                db.session.add(user)
                db.session.commit()

            # Export meter data

            for year in [2014, 2015, 2016]:
                for meter_id in range(1, 4):
                    Meter.exportCsvToDatabase(user, year, meter_id)

    @staticmethod
    def initiateDatabase(app):
        # Migrate database
        migrate = Migrate(app, db)

        # Initiate database
        db.init_app(app)
        with app.app_context():
            db.create_all()
        migrate.init_app(app, db)


if __name__ == "__main__":
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://app.sqlite'
    Database.importRelevantData(app)
