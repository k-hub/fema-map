from app import db, ma


class Fema(db.Model):
    __table__ = db.Model.metadata.tables['fema']

    def __repr__(self):
        return '<Disaster id={} fy_declared={} state={} incident_type={}>'.format(
            self.id, self.fy_declared, self.state, self.incident_type)


class State(db.Model):
    __tablename__ = 'geo_states'
    __bind_key__ = 'states'

    def __repr__(self):
        return '<State abbrev={} state={}'.format(
            self.abbrev, self.state)


class FemaSchema(ma.ModelSchema):
    class Meta:
        model = Fema
        fields = ('fy_declared', 'state', 'incident_type')


class StateSchema(ma.ModelSchema):
    class Meta:
        model = State
        fields = ('state', 'abbrev')
