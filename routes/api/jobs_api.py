from flask import jsonify, make_response, request
from routes.api import api_bp
from data.db import db
from data.__all_models import Jobs, Category, User
from configs.configs import login_required
from flask_security import current_user
import datetime


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


@api_bp.route('/jobs', methods=['POST'])
@login_required
def add_job():
    """Добавить новую работу"""
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)

    required_fields = ['job', 'team_leader', 'work_size']
    if not all(field in request.json for field in required_fields):
        return make_response(jsonify({'error': 'Missing required fields'}), 400)

    team_leader = db.session.get(User, request.json['team_leader'])
    if not team_leader:
        return make_response(jsonify({'error': 'Team leader not found'}), 404)

    job = Jobs(
        job=request.json['job'],
        team_leader=request.json['team_leader'],
        work_size=request.json['work_size'],
        start_date=datetime.datetime.now(),
        is_finished=request.json.get('is_finished', False)
    )

    db.session.add(job)

    if 'collaborators' in request.json:
        users = db.session.query(User).filter(
            User.id.in_(request.json['collaborators'])
        ).all()
        job.collaborators = users

    if 'categories' in request.json:
        categories = db.session.query(Category).filter(
            Category.id.in_(request.json['categories'])
        ).all()
        job.categories = categories

    db.session.commit()

    return jsonify({'id': job.id, 'success': 'Job created'}), 201


@api_bp.route('/jobs/<int:job_id>', methods=['PUT'])
@login_required
def update_job(job_id):
    """Обновить работу"""
    job = db.session.get(Jobs, job_id)
    if not job:
        return make_response(jsonify({'error': 'Job not found'}), 404)
    if not current_user.can_edit_job(job):
        return make_response(jsonify({'error': 'Permission denied'}), 403)
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)

    if 'job' in request.json:
        job.job = request.json['job']
    if 'team_leader' in request.json:
        team_leader = db.session.get(User, request.json['team_leader'])
        if not team_leader:
            return make_response(jsonify({'error': 'Team leader not found'}), 404)
        job.team_leader = request.json['team_leader']
    if 'work_size' in request.json:
        job.work_size = request.json['work_size']
    if 'is_finished' in request.json:
        job.is_finished = request.json['is_finished']
    if 'collaborators' in request.json:
        users = db.session.query(User).filter(
            User.id.in_(request.json['collaborators'])
        ).all()
        job.collaborators = users
    if 'categories' in request.json:
        categories = db.session.query(Category).filter(
            Category.id.in_(request.json['categories'])
        ).all()
        job.categories = categories

    db.session.commit()

    return jsonify({'id': job.id, 'success': 'Job updated'}), 200


@api_bp.route('/jobs/<int:job_id>', methods=['DELETE'])
@login_required
def delete_job(job_id):
    """Удалить работу"""
    job = db.session.get(Jobs, job_id)
    if not job:
        return make_response(jsonify({'error': 'Job not found'}), 404)
    if not current_user.can_edit_job(job):
        return make_response(jsonify({'error': 'Permission denied'}), 403)

    db.session.delete(job)
    db.session.commit()

    return jsonify({'id': job_id, 'success': 'Job deleted'}), 200
