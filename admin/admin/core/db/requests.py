from .utils import sql_task


@sql_task
def get_user(cursor, user_id: int):
    cursor.execute("SELECT * FROM Users WHERE id = %s;", (user_id,))
    row = cursor.fetchall()

    return row


@sql_task
def commit_user(cursor, user_id: int):
    cursor.execute("UPDATE Users SET is_admin = %s WHERE id = %s;", (True, user_id))


@sql_task
def check_user(cursor, user_id: int):
    cursor.execute("SELECT is_admin FROM Users WHERE id = %s;", (user_id,))
    row = cursor.fetchall()
    try:
        user = row[0][0]
    except:
        user = False

    return user


@sql_task
def get_help(cursor, order_id: str):
    cursor.execute(
        "SELECT o.work_date, o.discipline, o.format, o.work_time, o.comment, u.username, u.first_name, u.last_name, u.uni, u.study_year, o.user_id FROM orderhelp as o, users as u WHERE o.id = %s AND u.id = o.user_id;",
        (order_id,),
    )
    row = cursor.fetchall()

    return row[0]


@sql_task
def get_work(cursor, order_id: str):
    cursor.execute(
        "SELECT o.work_date, o.discipline, o.theme, o.volume, o.unique_persentage, o.order_type, o.comment, o.file_names, u.username, u.first_name, u.last_name, u.uni, u.study_year, o.user_id FROM orderwork as o, users as u WHERE o.id = %s AND u.id = o.user_id;",
        (order_id,),
    )
    row = cursor.fetchall()

    return row[0]


@sql_task
def get_tutoring(cursor, tutoring_id: str):
    cursor.execute(
        "SELECT t.study_type, t.study_name, t.study_year, t.lessons, t.tutor_sex, t.comment, u.username, u.first_name, u.last_name FROM tutoring as t, users as u WHERE t.id = %s AND t.user_id = u.id;",
        (tutoring_id,),
    )
    row = cursor.fetchall()

    return row[0]


@sql_task
def get_admins(cursor):
    cursor.execute("SELECT id FROM Users WHERE is_admin = %s", (True,))
    row = cursor.fetchall()

    return row


@sql_task
def get_works(cursor, start, end):
    cursor.execute(
        "SELECT * FROM orderwork where created_at between %s and %s;", (start, end)
    )
    row = cursor.fetchall()

    return row


@sql_task
def get_helps(cursor, start, end):
    cursor.execute(
        "SELECT * FROM orderhelp where created_at between %s and %s;", (start, end)
    )
    row = cursor.fetchall()

    return row


@sql_task
def get_users_num(cursor):
    cursor.execute("SELECT count(*) FROM Users")
    row = cursor.fetchall()

    return row
