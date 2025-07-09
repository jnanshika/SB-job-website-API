from app.extensions import db
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from app.utils import send_email
from app.models import UserModel, JobModel


class ApplicationService:
    @staticmethod
    def create_application(application):
        try: 
            db.session.add(application)
            db.session.commit()
            
            # Email Notification Logic 
            user = UserModel.query.get(application.user_id)
            job = JobModel.query.get(application.job_id)
            recruiter = UserModel.query.get(job.posted_by)

            # Email to recruiter
            recruiter_subject = f"New Application for {job.title}"
            recruiter_body = f"{user.name} has applied to your job '{job.title}'."
            send_email(recruiter_subject, recruiter_body, [recruiter.email])

            # Email to candidate
            candidate_subject = f"Application Submitted for {job.title}"
            candidate_body = f"You have successfully applied to '{job.title}'."
            send_email(candidate_subject, candidate_body, [user.email])
            return {"message": "Application submitted successfully"}, 201
        
        except IntegrityError as e:
            db.session.rollback()
            # Check for unique constraint failure
            if "unique_application" in str(e.orig):
                return jsonify({"error": "You have already applied to this job."}), 409
            return jsonify({"error": "Database integrity error."}), 500

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500