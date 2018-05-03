from app import db, ma


class Fema(db.Model):
    __table__ = db.Model.metadata.tables['fema']

    def __repr__(self):
        return '<Disaster id={} date={} state={} incident_type={}>'.format(
            self.id, self.incident_begin_date, self.state, self.incident_type)


class FemaSchema(ma.ModelSchema):
    class Meta:
        model = Fema
