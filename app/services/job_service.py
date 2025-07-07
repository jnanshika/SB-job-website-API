from app.models import UserModel, JobModel
from app.extensions import db
from app.schemas import JobSchema

class JobService():

    @staticmethod
    def create_job(data):
        db.session.add(data)
        db.session.commit()

        return {"message": "Job was sccessfully added!"}, 201