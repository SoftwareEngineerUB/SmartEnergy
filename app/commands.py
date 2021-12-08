import click
from app.main import app
from app.models import Data, Device, User, db
from app.main import db


@app.cli.command('import-data')
@click.argument('path')
@click.argument('user', required=False)
@click.argument('rows', required=False)
def import_data(path, user=None, rows=100):
    """
        Imports mock data from the CSV file
    """

    if user is None:
        user = User(username='import', email='import@smartenergy.cloud')
        user.set_password('password')
        db.session.add(user)
    else:
        user = db.session.query(User).filter_by(username=user).one()

    with open(path, 'r') as file:
        header = file.readline()
        content = file.readlines(rows)
        # TODO: insert data in database like the above user example

    db.session.commit()
    print('Done')
