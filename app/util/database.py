from flask import Flask
from flask_migrate import Migrate
from random import random
from datetime import datetime
from dateutil.parser import parse

from app.device.meter import Meter
from app.models import User, Device, Data, Event
from app.models.db import db


class Database:
    @staticmethod
    def importRelevantData(app, testing=False):
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

        if not testing:
            for year in [2014, 2015, 2016]:
                for meter_id in range(1, 4):
                    if meter_id == 3 and year == 2014:
                        continue
                    Meter.exportCsvToDatabase(user, year, meter_id)

    @staticmethod
    def cleanDatabase():
        # If the database is not the test one, avoid using this
        if str(db.engine.url).find('app-test.sqlite') == -1:
            raise RuntimeError()

        db.session.query(Device).delete()
        db.session.query(Data).delete()
        db.session.query(Event).delete()
        db.session.query(User).delete()
        db.session.commit()

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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../app.sqlite'
    Database.importRelevantData(app)
