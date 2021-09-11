from .utils import sql_task


@sql_task
def get_user(cursor, user_id: int):
    cursor.execute("SELECT * FROM Users WHERE id = %s;", (user_id,))
    row = cursor.fetchall()

    return row


@sql_task
def post_user(cursor, user: dict):
    cursor.execute(
        "INSERT INTO Users(id, username, first_name, last_name) VALUES (%s, %s, %s, %s);",
        (
            user["id"],
            user["username"],
            user["first_name"],
            user["last_name"],
        ),
    )

    return True


@sql_task
def post_work(cursor, order: dict):
    cursor.execute(
        "INSERT INTO orderwork(id, work_date, user_id, discipline, theme, volume, unique_persentage, comment, order_type, file_names) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
        (
            order["id"],
            order["work_date"],
            order["user_id"],
            order["discipline"],
            order["theme"],
            order["volume"],
            order["unique_persentage"],
            order["comment"],
            order["order_type"],
            order["file_names"],
        ),
    )


@sql_task
def post_help(cursor, order: dict):
    cursor.execute(
        "INSERT INTO orderhelp(id, work_date, user_id, discipline, format, comment, work_time) VALUES (%s, %s, %s, %s, %s, %s, %s);",
        (
            order["id"],
            order["work_date"],
            order["user_id"],
            order["discipline"],
            order["format"],
            order["comment"],
            order["work_time"],
        ),
    )


@sql_task
def post_tutor(cursor, order: dict):
    cursor.execute(
        "INSERT INTO Tutoring (id, study_type, study_name, user_id, study_year, lessons, tutor_sex, comment) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
        (
            order["id"],
            order["study_type"],
            order["study_name"],
            order["user_id"],
            order["study_year"],
            order["lessons"],
            order["tutor_sex"],
            order["comment"],
        ),
    )


@sql_task
def update_uni(cursor, uni: str, user_id: int):
    cursor.execute("UPDATE users SET uni = %s WHERE id = %s;", (uni, user_id))


@sql_task
def update_year(cursor, year: str, user_id: int):
    cursor.execute("UPDATE users SET study_year = %s WHERE id = %s;", (year, user_id))


@sql_task
def check_uni(cursor, user_id: int):
    cursor.execute("SELECT uni FROM Users WHERE id = %s;", (user_id,))
    row = cursor.fetchall()

    return row


@sql_task
def check_year(cursor, user_id: int):
    cursor.execute("SELECT study_year FROM Users WHERE id = %s;", (user_id,))
    row = cursor.fetchall()

    return row
