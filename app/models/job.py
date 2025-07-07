from app.extensions import db

class JobModel(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key =True  ,nullable = False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    posted_by = db.Column(db.Integer, db.ForeignKey('users.id') , nullable=False)
    location = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    applications = db.relationship('ApplicationModel', back_populates='job', cascade='all, delete-orphan')
