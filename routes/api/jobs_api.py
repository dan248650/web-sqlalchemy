from flask import jsonify, make_response
from routes.api import api_bp
from data.db import db
from data.__all_models import Jobs


@api_bp.route('/jobs', methods=['GET'])
def get_jobs():
    """Получить список всех работ"""
    jobs = db.session.query(Jobs).all()
    return jsonify({
        'jobs': [job.to_dict() for job in jobs]
    })


@api_bp.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Получить одну работу по ID"""
    job = db.session.get(Jobs, job_id)
    if not job:
        return make_response(jsonify({'error': 'Job not found'}), 404)
    return jsonify({
        'job': job.to_dict()
    })
