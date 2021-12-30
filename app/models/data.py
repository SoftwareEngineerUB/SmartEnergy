from .db import db


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime(), nullable=False)
    value = db.Column(db.Float(), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id', ondelete='cascade'))

    def __repr__(self):
        return '<Device %r %r>' % (self.alias, self.uuid)
