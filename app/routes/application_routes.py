from flask import Blueprint, request
from app.schemas import ApplicationSchema, ValidationError
from app.extensions import db
from app.models import ApplicationModel, UserModel, JobModel
from app.services import ApplicationService
from app.utils import candidate_required, recruiter_required

application_routes = Blueprint('application_routes', __name__)

@application_routes.route('/apply/<int:job_id>', methods=['POST'])
@candidate_required
def create_application(candidate_record, job_id):
    jsonData = request.get_json()
    if not candidate_record or candidate_record.status != 'active':
        return {"error": "Inactive or invalid candidate"}, 403

    job = JobModel.query.filter_by(id= job_id).first()
    if not job or job.status != 'Active' :
        return {"error": "Inactive or invalid job"}, 403

    try: 
        app_schema = ApplicationSchema(session = db.session, partial = True)  
        application = app_schema.load(jsonData)  
        application.user_id = candidate_record.id
        application.job_id = job_id

    except ValidationError as error:
        return {"errors": error.messages}, 400

    return ApplicationService.create_application(application)

@application_routes.route('/getapplications/<int:job_id>', methods=['GET'])
@recruiter_required
def get_applications(recruiter, job_id):
    job = JobModel.query.get(job_id)
    if not job:
        return {"error": "Job not found"}, 404

    if job.posted_by != recruiter.id:
        return {"error" : f"This job was not posted by {recruiter.name}"}

    applications = ApplicationModel.query.filter_by(job_id = job_id).all()
    if not applications: 
        return {"message": "No application was found"} , 200
    
    try: 
        result = ApplicationSchema(many=True).dump(applications)
        return {"job applications": result}, 200    
    except ValidationError as error:
        return {"errors": error.messages}, 400

@application_routes.route('/user-applied-job/<int:user_id>', methods=['GET'])
@candidate_required
def get_userappliedjob(candidate_record, user_id):
    user = UserModel.query.get(user_id)
    if not user:
        return {"error": "User not found"}, 404

    applications = ApplicationModel.query.filter_by(user_id = user_id).all()
    if not applications: 
        return {"message": f"No application done by {user.name} found"} , 500
    
    try: 
        result = ApplicationSchema(many=True).dump(applications)
        return {"user applications": result}, 200    
    except ValidationError as error:
        return {"errors": error.messages}, 400
    