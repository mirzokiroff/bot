from datetime import datetime
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

    async def add_user(self, full_name=None, username=None, phone_number=None, confirmation_code=None, telegram_id=None,
                       language=None, location=None, password=None, is_superuser=False, first_name=None, last_name=None,
                       email=None, is_staff=False, is_active=True, date_joined=None, last_login=None):
        location_str = f"{location.latitude},{location.longitude}"
        # Bazada bu usernameni tekshirish
        user_exists = await self.select_user_by_username(username)
        if user_exists:
            # Bazada foydalanuvchi allaqachon mavjud
            # Agar foydalanuvchi allaqachon mavjud bo'lsa, uni yangilash kerak
            sql = """
            UPDATE users_user SET full_name=$1, phone_number=$2, confirmation_code=$3, telegram_id=$4, password=$5,
            is_superuser=$6, first_name=$7, last_name=$8, email=$9, is_staff=$10, is_active=$11, date_joined=$12, 
            language=$13, location=$14, last_login=$15 WHERE username=$16
            """
            result = await self.execute(sql, full_name, phone_number, confirmation_code, telegram_id, password,
                                        is_superuser, first_name, last_name, email, is_staff, is_active, date_joined,
                                        language, location_str, last_login, username,
                                        execute=True)
        else:
            # Bazada foydalanuvchi mavjud emas
            # Yangi foydalanuvchi qo'shish
            sql = """
            INSERT INTO users_user (full_name, username, language, phone_number, confirmation_code, telegram_id, 
                                    password, is_superuser, first_name, last_name, email, is_staff, is_active, 
                                    date_joined, last_login, location)
            VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16) returning *
            """
            result = await self.execute(sql, full_name, username, language, phone_number, confirmation_code,
                                        telegram_id, password, is_superuser, first_name, last_name, email, is_staff,
                                        is_active, date_joined, last_login, location_str,
                                        fetchrow=True)
        return result

    async def update_users(self, new_full_name, new_username, new_phone_number, new_confirmation_code, new_telegram_id,
                           new_language, new_location, new_password, new_is_superuser, new_first_name, new_last_name,
                           new_email, new_is_staff, new_is_active, new_date_joined, new_last_login):
        sql = (
            "UPDATE users_user SET full_name=$1, username=$2, language=$3, location=$4, phone_number=$5, "
            "confirmation_code=$6, telegram_id=$7, password=$8, is_superuser=$9, is_active=$10, first_name=$11, "
            "last_name=$12, email=$13, is_staff=$14, date_joined=$15, last_login=$16 WHERE id=$17")
        return await self.execute(sql, new_full_name, new_username, new_phone_number, new_confirmation_code,
                                  new_telegram_id, new_language, new_location, new_password, new_is_superuser,
                                  new_first_name, new_last_name, new_email, new_is_staff, new_is_active,
                                  new_date_joined, new_last_login, execute=True)

    async def select_all_users(self):
        sql = "SELECT * FROM users_user"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM users_user WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_user_phone(self, **kwargs):
        sql = "SELECT phone_number FROM users_user WHERE"
        sql, parameters = self.format_args(sql, parameters=kwargs)

        async with self.pool.acquire() as connection:
            async with connection.transaction():
                phone_numbers = await connection.fetch(sql, *parameters)
                return [record['phone_number'] for record in phone_numbers]

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

    async def add_restaurant(self, name, location_latitude, location_longitude, location_text, location_video):
        sql = (
            "INSERT INTO users_restaurant (name, location_latitude, location_longitude, location_text, location_video)"
            " VALUES($1, $2, $3, $4, $5) returning *"
        )
        return await self.execute(sql, name, location_latitude, location_longitude, location_text, location_video,
                                  fetchrow=True)

    async def select_all_restaurant(self):
        sql = "SELECT * FROM users_restaurant"
        return await self.execute(sql, fetch=True)

    async def select_restaurant(self, **kwargs):
        sql = "SELECT * FROM users_restaurant WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def update_course(self, new_name, new_location_text, new_location_latitude, new_location_longitude,
                            new_location_video):
        sql = ("UPDATE users_restaurant SET name=$1, location_latitude=$2, location_longitude=$3, location_text=$4, "
               "location_video=$5 WHERE id=$6")
        return await self.execute(sql, new_name, new_location_text, new_location_latitude, new_location_longitude,
                                  new_location_video, execute=True)

    async def delete_course(self, course_id):
        sql = "DELETE FROM users_restaurant WHERE id=$1"
        return await self.execute(sql, course_id, execute=True)
