from data.db_session import global_init, create_session
from data.__all_models import User


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


if __name__ == '__main__':
    db_name = input().strip()
    global_init(db_name)

    get_not_engineers_from_module1()
