from data.db_session import global_init, create_session
from data.__all_models import User, Jobs


def get_colonists_from_module1():
    """
    Подключается к базе данных и выводит всех колонистов из первого модуля
    """
    db_sess = create_session()

    colonists = db_sess.query(User).filter(User.address == 'module_1').all()

    print(*colonists, sep='\n')

    return colonists


def get_not_engineers_from_module1():
    """
    Подключается к базе данных и выводит id колонистов из первого модуля,
    у которых ни speciality, ни position не содержат подстроку 'engineer'
    """
    db_sess = create_session()

    colonists_ids = db_sess.query(User.id).filter(
        User.address == 'module_1',
        ~User.speciality.contains('engineer'),
        ~User.position.contains('engineer')
    ).all()

    [print(colonist_id[0]) for colonist_id in colonists_ids]

    return colonists_ids


def get_minor_colonists():
    """
    Подключается к базе данных и выводит несовершеннолетних
    колонистов с указанием возраста
    """
    db_sess = create_session()

    colonists = db_sess.query(User).filter(User.age < 18).all()

    [print(colonist, colonist.age, "years") for colonist in colonists]

    return colonists


def get_chief_and_middle_colonists():
    """
    Подключается к базе данных и выводит колонистов,
    у которых в названии должности (position) есть chief или middle
    """
    db_sess = create_session()

    colonists = db_sess.query(User).filter(
        User.position.contains('chief') |
        User.position.contains('middle')
    ).all()

    [print(colonist, colonist.position) for colonist in colonists]

    return colonists


def get_filtered_jobs():
    """
    Подключается к базе данных и выводит актуальные работы,
    выполнение которых требует меньше 20 часов
    """
    db_sess = create_session()

    jobs = db_sess.query(Jobs).filter(
        Jobs.work_size < 20,
        ~Jobs.is_finished
    ).all()

    [print(job) for job in jobs]

    return jobs


def get_team_leaders_of_largest_teams():
    """
    Подключается к базе данных и выводит фамилии и имена тимлидов работ,
    которые выполняются наибольшими командами
    """
    db_sess = create_session()

    all_jobs = db_sess.query(Jobs).all()

    max_size = 0
    for job in all_jobs:
        team_size = 0
        if job.collaborators and job.collaborators.strip():
            team_size = len(job.collaborators.split(','))
        team_size += 1
        max_size = max(max_size, team_size)

    jobs_with_max_team = []
    for job in all_jobs:
        team_size = 1
        if job.collaborators and job.collaborators.strip():
            team_size += len(job.collaborators.split(','))
        if team_size == max_size:
            jobs_with_max_team.append(job)

    selected_leaders = []
    for job in jobs_with_max_team:
        team_leader = db_sess.query(User).filter(User.id == job.team_leader).first()
        if team_leader:
            selected_leaders.append(f"{team_leader.name} {team_leader.surname}")

    [print(name) for name in set(selected_leaders)]

    return selected_leaders


def update_address_for_young_colonists():
    """
    Подключается к базе данных и изменяет адрес на 'module_3' для всех колонистов,
    проживающих в module_1 и имеющих возраст менее 21 года
    """
    db_sess = create_session()

    colonists_to_update = db_sess.query(User).filter(
        User.address == 'module_1',
        User.age < 21
    ).all()

    for colonist in colonists_to_update:
        colonist.address = 'module_3'

    db_sess.commit()

    return colonists_to_update


if __name__ == '__main__':
    db_name = input().strip()
    global_init(db_name)

    pass
