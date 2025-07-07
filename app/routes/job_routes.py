from flask import Blueprint, request
from app.schemas import JobSchema, ValidationError
from app.services import JobService, AuthService
from app.models import JobModel, UserModel
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.extensions import db
from app.utils import token_required, candidate_required, recruiter_required

job_routes = Blueprint('job_routes', __name__)

@job_routes.route('/new',methods=['POST'])
@recruiter_required
def create_job(user):
    jsonData = request.get_json()
    if 'posted_by' in jsonData :
        return {"message" : "You cannot set posted by manually"}, 400
    
    try: 
        job_schema = JobSchema(session = db.session)  
        jobData = job_schema.load(jsonData)
        jobData.posted_by = user.id
    except ValidationError as error:
        return {"errors": error.messages}, 400
    
    return JobService.create_job(jobData)


@job_routes.route('/', methods=['GET'])
def get_alljobs():
    jobs = JobModel.query.all()
    if not jobs:
        return {"message": "No jobs found"}, 200
    
    try: 
        job_schema = JobSchema(many= True)
    
    except ValidationError as error:
        return {"errors": error.messages}, 400

    return { "jobs:" :job_schema.dump(jobs) }, 200
