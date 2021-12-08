from .db import db


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime(), nullable=False)
    mention = db.Column(db.String(255))
    device_id = db.Column(db.Integer, db.ForeignKey('data.id', ondelete='cascade'))

    def __repr__(self):
        return '<Device %r %r>' % (self.alias, self.uuid)
