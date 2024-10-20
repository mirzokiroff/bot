from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
            port=config.DB_PORT
        )

    async def execute(
            self,
            command,
            *args,
            fetch: bool = False,
            fetchval: bool = False,
            fetchrow: bool = False,
            execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def select_user_by_username(self, username):
        sql = "SELECT * FROM users_user WHERE username = $1"
        return await self.execute(sql, username, fetchrow=True)

    async def add_user(self, full_name=None, username=None, phone_number=None, phone_number2=None, activity=None,
                       telegram_id=None, language=None,
                       password=None, is_superuser=False, first_name=None, last_name=None, email=None,
                       is_staff=False, is_active=True, date_joined=None):
        # Bazada bu usernameni tekshirish
        user_exists = await self.select_user_by_username(username)
        if user_exists:
            # Bazada foydalanuvchi allaqachon mavjud
            # Agar foydalanuvchi allaqachon mavjud bo'lsa, uni yangilash kerak
            sql = """
            UPDATE users_user SET full_name=$1, phone_number=$2, phone_number2=$3, activity=$4, telegram_id=$5, password=$6,
            is_superuser=$7, first_name=$8, last_name=$9, email=$10, is_staff=$11, is_active=$12, date_joined=$13, language=$14
            WHERE username=$15
            """
            result = await self.execute(sql, full_name, phone_number, phone_number2, activity, telegram_id, password,
                                        is_superuser,
                                        first_name, last_name, email, is_staff, is_active, date_joined, language,
                                        username,
                                        execute=True)
        else:
            # Bazada foydalanuvchi mavjud emas
            # Yangi foydalanuvchi qo'shish
            sql = """
            INSERT INTO users_user (full_name, username, language, phone_number, phone_number2, activity, telegram_id, password, is_superuser, 
                                    first_name, last_name, email, is_staff, is_active, date_joined)
            VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15) returning *
            """
            result = await self.execute(sql, full_name, username, language, phone_number, phone_number2, activity,
                                        telegram_id,
                                        password,
                                        is_superuser, first_name, last_name, email, is_staff, is_active, date_joined,
                                        fetchrow=True)
        return result

    async def select_all_users(self):
        sql = "SELECT * FROM users_user"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM users_user WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM users_user"
        return await self.execute(sql, fetchval=True)

    async def update_user(self, user_id, **kwargs):
        sql = "UPDATE users_user SET "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        sql += f" WHERE id=${len(parameters) + 1}"
        parameters += (user_id,)
        return await self.execute(sql, *parameters, execute=True)

    async def delete_user(self, user_id):
        sql = "DELETE FROM users_user WHERE id=$1"
        return await self.execute(sql, user_id, execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE users_user", execute=True)

    #

    async def add_course(self, course_name):
        sql = ("INSERT INTO users_course (course_name)"
               " VALUES($1) returning *")
        return await self.execute(sql, course_name, fetchrow=True)

    async def select_all_courses(self):
        sql = "SELECT * FROM users_course"
        return await self.execute(sql, fetch=True)

    async def select_course_video(self, course_name):
        sql = "SELECT course_video FROM users_course WHERE course_name = $1"
        return await self.execute(sql, course_name, fetchrow=True)

    async def select_course(self, **kwargs):
        sql = "SELECT * FROM users_course WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_courses(self):
        sql = "SELECT COUNT(*) FROM users_course"
        return await self.execute(sql, fetchval=True)

    async def update_course(self, course_id, new_course_name):
        sql = "UPDATE users_course SET course_name=$1 WHERE id=$2"
        return await self.execute(sql, new_course_name, execute=True)

    async def delete_course(self, course_id):
        sql = "DELETE FROM users_course WHERE id=$1"
        return await self.execute(sql, course_id, execute=True)

    #

    async def add_course_media(self, course_video=True, course_text=True, course_photo=True, course_pdf=True,
                               media_id=True):
        sql = ("INSERT INTO users_coursemedia (course_video, course_text, course_photo, course_pdf, media_id)"
               " VALUES($1, $2, $3, $4, $5) returning *")
        return await self.execute(sql, course_video, course_text, course_photo, course_pdf, media_id, fetchrow=True)

    async def select_all_courses_media(self):
        sql = "SELECT * FROM users_coursemedia"
        return await self.execute(sql, fetch=True)

    async def select_course_media(self, **kwargs):
        sql = "SELECT * FROM users_coursemedia WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_courses_media(self):
        sql = "SELECT COUNT(*) FROM users_coursemedia"
        return await self.execute(sql, fetchval=True)

    async def update_course_media(self, course_id, new_course_video, new_course_text, new_coruse_pdf,
                                  new_course_photo, new_media_id):
        sql = "UPDATE users_coursemedia SET course_video=$1, course_text=$2, course_photo=$3, course_pdf=$4, media_id=$5 WHERE id=$6"
        return await self.execute(sql, new_course_video, new_course_text, course_id, new_coruse_pdf,
                                  new_course_photo, new_media_id, execute=True)

    async def delete_course_media(self, course_id):
        sql = "DELETE FROM users_coursemedia WHERE id=$1"
        return await self.execute(sql, course_id, execute=True)

    #

    async def user_add_course(self, course_name, course_type, user_name, user_phone_number, user_phone_number2, date_joined):
        sql = (
            "INSERT INTO users_user_course (course_name, course_type, user_name, user_phone_number, user_phone_number2, date_joined)"
            " VALUES($1, $2, $3, $4, $5, $6) returning *")
        return await self.execute(sql, course_name, course_type, user_name, user_phone_number, user_phone_number2, date_joined,
                                  fetchrow=True)

    async def user_select_all_courses(self):
        sql = "SELECT * FROM users_user_course"
        return await self.execute(sql, fetch=True)

    async def user_select_course(self, **kwargs):
        sql = "SELECT * FROM users_user_course WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def user_count_courses(self):
        sql = "SELECT COUNT(*) FROM users_user_course"
        return await self.execute(sql, fetchval=True)

    async def user_update_course(self, course_id, new_course_name, new_course_type, new_user_name,
                                 new_user_phone_number, new_user_phone_number2, date_joined):
        sql = "UPDATE users_user_course SET course_name=$1, course_type=$2, user_name=$3, user_phone_number=$4, user_phone_number2=$5, date_joined=$6 WHERE id=$7"
        return await self.execute(sql, new_course_name, new_course_type, new_user_name, new_user_phone_number,
                                  new_user_phone_number2, date_joined,
                                  course_id, execute=True)

    async def user_delete_course(self, course_id):
        sql = "DELETE FROM users_user_course WHERE id=$1"
        return await self.execute(sql, course_id, execute=True)

    #

    async def add_about_edu(self, edu_photo=True, description=None):
        sql = "INSERT INTO users_about_edu (edu_photo, description) VALUES($1, $2) RETURNING *"
        return await self.execute(sql, edu_photo, description, fetchrow=True)

    async def select_all_edu(self):
        sql = "SELECT * FROM users_about_edu"
        return await self.execute(sql, fetch=True)

    async def select_about_edu(self, **kwargs):
        sql = "SELECT * FROM users_about_edu WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_about_edu_description(self):
        sql = "SELECT description, edu_photo FROM users_about_edu"
        return await self.execute(sql, fetch=True)

    async def update_about_edu(self, about_edu_id, new_description, new_edu_photo):
        sql = "UPDATE users_about_edu SET description=$1, edu_photo=$2 WHERE id=$3"
        return await self.execute(sql, new_description, new_edu_photo, about_edu_id, execute=True)

    async def delete_about_edu(self, about_edu_id):
        sql = "DELETE FROM users_about_edu WHERE id=$1"
        return await self.execute(sql, about_edu_id, execute=True)

    #

    async def add_about_edu_media(self, video=True, photo=True, media_id=True):
        sql = "INSERT INTO users_about_edu_media (video, photo, media_id) VALUES($1, $2, $3) RETURNING *"
        return await self.execute(sql, video, photo, media_id, fetchrow=True)

    async def select_all_edu_media(self):
        sql = "SELECT * FROM users_about_edu_media"
        return await self.execute(sql, fetch=True)

    async def select_about_edu_media(self, **kwargs):
        sql = "SELECT * FROM users_about_edu_media WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_about_edu_media_video(self):
        sql = "SELECT photo, video, media_id FROM users_about_edu_media"
        return await self.execute(sql, fetch=True)

    async def update_about_edu_media(self, about_edu_id, new_video, new_photo, new_media_id):
        sql = "UPDATE users_about_edu_media SET photo=$1, video=$2, media_id=$3 WHERE id=$4"
        return await self.execute(sql, new_video, new_photo, new_media_id, about_edu_id, execute=True)

    async def delete_about_edu_media(self, about_edu_id):
        sql = "DELETE FROM users_about_edu_media WHERE id=$1"
        return await self.execute(sql, about_edu_id, execute=True)

    #

    async def add_contact_us(self, phone_number=None, telegram_admin=None, telegram_chanel=None, instagram=None,
                             you_tube=None, email=None):
        sql = "INSERT INTO users_contact_us (phone_number, telegram_admin, telegram_chanel, instagram, you_tube, email) VALUES($1, $2, $3, $4, $5, $6) returning *"
        return await self.execute(sql, phone_number, telegram_admin, telegram_chanel, instagram, you_tube, email,
                                  fetchrow=True)

    async def select_contact_us(self):
        sql = "SELECT * FROM users_contact_us"
        return await self.execute(sql, fetch=True)

    async def update_contact_us(self, contact_us_id, new_phone_number, new_telegram_admin, new_telegram_chanel,
                                new_instagram, new_you_tube,
                                new_email):
        sql = "UPDATE users_contact_us SET phone_number=$1, telegram_admin=$2,, telegram_chanel=$3, instagram=$4, you_tube=$5, email=$6 WHERE id=$7"
        return await self.execute(sql, new_phone_number, new_telegram_admin, new_telegram_chanel, new_instagram,
                                  new_you_tube, new_email,
                                  contact_us_id, execute=True)

    async def delete_contact_us(self, contact_us_id):
        sql = "DELETE FROM users_contact_us WHERE id=$1"
        return await self.execute(sql, contact_us_id, execute=True)

    #

    async def add_location_edu(self, location_latitude=None, location_longitude=None, location_text=None,
                               location_video=None):
        sql = "INSERT INTO users_location_edu (location_latitude, location_longitude, location_text, location_video) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, location_latitude, location_longitude, location_text, location_video,
                                  fetchrow=True)

    async def select_location_edu(self):
        sql = "SELECT * FROM users_location_edu"
        return await self.execute(sql, fetch=True)

    async def update_location_edu(self, location_edu_id, new_location_latitude, new_location_longitude,
                                  new_location_text, new_location_video):
        sql = "UPDATE users_location_edu SET location_latitude=$1, location_longitude=$2, location_text=$3, location_video=$4 WHERE id=$5"
        return await self.execute(sql, new_location_latitude, new_location_longitude, new_location_text,
                                  location_edu_id,
                                  new_location_video, execute=True)

    async def delete_location_edu(self, location_edu_id):
        sql = "DELETE FROM users_location_edu WHERE id=$1"
        return await self.execute(sql, location_edu_id, execute=True)
