from flask_restful import Resource, abort
from flask_security import current_user
from data.db import db
from data.__all_models import Jobs, User, Category
from configs.configs import login_required
from routes.api.v2.parsers.job_parser import job_parser, job_update_parser
import datetime


class JobsListResource(Resource):
    method_decorators = [login_required]

    def get(self):
        jobs = db.session.query(Jobs).all()
        return {
            'jobs': [job.to_dict() for job in jobs]
        }, 200

    def post(self):
        args = job_parser().parse_args()

        team_leader = db.session.get(User, args['team_leader'])
        if not team_leader:
            abort(404, error='Team leader not found',
                  message=f'Руководитель с id {args["team_leader"]} не найден')

        job = Jobs(
            job=args['job'],
            team_leader=args['team_leader'],
            work_size=args['work_size'],
            is_finished=args.get('is_finished', False)
        )

        if args.get('start_date'):
            try:
                job.start_date = datetime.datetime.strptime(args['start_date'], '%Y-%m-%d').date()
            except ValueError:
                abort(400, error='Invalid date format',
                      message='start_date должен быть в формате YYYY-MM-DD')
        else:
            job.start_date = datetime.datetime.now().date()

        if args.get('end_date'):
            try:
                job.end_date = datetime.datetime.strptime(args['end_date'], '%Y-%m-%d').date()
            except ValueError:
                abort(400, error='Invalid date format',
                      message='end_date должен быть в формате YYYY-MM-DD')

        db.session.add(job)

        if args.get('collaborators'):
            collaborators = db.session.query(User).filter(
                User.id.in_(args['collaborators'])
            ).all()
            job.collaborators = collaborators

        if args.get('categories'):
            categories = db.session.query(Category).filter(
                Category.id.in_(args['categories'])
            ).all()
            job.categories = categories

        db.session.commit()

        return {
            'id': job.id,
            'job': job.job,
            'success': 'Job created',
            'message': 'Работа успешно создана'
        }, 201


class JobsResource(Resource):
    method_decorators = [login_required]

    def get(self, job_id):
        job = db.session.get(Jobs, job_id)
        if not job:
            abort(404, error='Job not found',
                  message=f'Работа с id {job_id} не найдена')

        return {'job': job.to_dict()}, 200

    def put(self, job_id):
        job = db.session.get(Jobs, job_id)
        if not job:
            abort(404, error='Job not found',
                  message=f'Работа с id {job_id} не найдена')

        if not current_user.can_edit_job(job):
            abort(403, error='Permission denied',
                  message='У вас нет прав для редактирования этой работы')

        args = job_update_parser().parse_args()

        if args.get('job'):
            job.job = args['job']

        if args.get('team_leader'):
            team_leader = db.session.get(User, args['team_leader'])
            if not team_leader:
                abort(404, error='Team leader not found',
                      message=f'Руководитель с id {args["team_leader"]} не найден')
            job.team_leader = args['team_leader']

        if args.get('work_size'):
            job.work_size = args['work_size']

        if args.get('is_finished') is not None:
            job.is_finished = args['is_finished']

        if args.get('start_date'):
            try:
                job.start_date = datetime.datetime.strptime(args['start_date'], '%Y-%m-%d').date()
            except ValueError:
                abort(400, error='Invalid date format',
                      message='start_date должен быть в формате YYYY-MM-DD')

        if args.get('end_date'):
            try:
                job.end_date = datetime.datetime.strptime(args['end_date'], '%Y-%m-%d').date()
            except ValueError:
                abort(400, error='Invalid date format',
                      message='end_date должен быть в формате YYYY-MM-DD')

        if args.get('collaborators') is not None:
            collaborators = db.session.query(User).filter(
                User.id.in_(args['collaborators'])
            ).all()
            job.collaborators = collaborators

        if args.get('categories') is not None:
            categories = db.session.query(Category).filter(
                Category.id.in_(args['categories'])
            ).all()
            job.categories = categories

        db.session.commit()

        return {
            'success': 'Job updated',
            'message': 'Работа успешно обновлена',
            'job': job.to_dict(only=('id', 'job', 'team_leader', 'work_size', 'is_finished'))
        }, 200

    def delete(self, job_id):
        job = db.session.get(Jobs, job_id)
        if not job:
            abort(404, error='Job not found',
                  message=f'Работа с id {job_id} не найдена')

        if not current_user.can_edit_job(job):
            abort(403, error='Permission denied',
                  message='У вас нет прав для удаления этой работы')

        db.session.delete(job)
        db.session.commit()

        return {
            'success': 'Job deleted',
            'message': f'Работа "{job.job}" успешно удалена'
        }, 200
