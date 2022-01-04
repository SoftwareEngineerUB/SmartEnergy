import click
from app.models import User
from app.models.db import db
from app.device.meter import Meter
from flask import Blueprint

mock_blueprint = Blueprint('mock', __name__)


@mock_blueprint.cli.command('import-data')
@click.argument('year')
@click.argument('meter')
def import_data(year=2016, meter=1):
    """
        Imports mock data from the CSV file
    """

    username = 'mock-user-' + str(meter)
    user = db.session.query(User).filter_by(username=username).first()
    if user is None:
        user = User(username=username, email=username + '@smartenergy.cloud')
        user.set_password('password')
        db.session.add(user)

    Meter.load_data(user, year, meter)
    db.session.commit()
    print('Done')
