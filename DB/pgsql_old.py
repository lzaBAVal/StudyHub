
import asyncio

import asyncpg

from log.logging_core import init_logger

logger = init_logger()


class Database:
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.pool = loop.run_until_complete(
            asyncpg.create_pool(
                user='postgres',
                password='Cyberark!123',
                database='studyhubdb',
                host='23.105.226.171',
                port='5432'
            )
        )

    @staticmethod
    def formar_args(sql, parameters: dict):
        sql += ' AND '.join([
            f'{item} = ${num}' for num, item in enumerate(parameters, start=1)
        ])
        return sql, tuple(parameters.values())

    #########################
    #        CHECK          #
    #########################

    async def check_lock_group(self, chat_id: int, group_id: int) -> str:
        sql_query = "select lock from groups_students where id = $1"
        logger.info(f'Student - {chat_id} check lock group')
        return await self.pool.fetch(sql_query, group_id)

    '''
    async def check_ban(self, chat_id: int) -> str:
        sql_query = "select ban from student where chat_id = $1"
        logger.info(f'Student - {chat_id} check_ban')
        return await self.pool.fetch(sql_query, chat_id)
    '''

    async def check_user(self, chat_id: int) -> str:
        sql_query = "select * from student where chat_id = $1"
        logger.info(f'Student - {chat_id} check_user')
        return await self.pool.fetch(sql_query, chat_id)

    async def check_tester(self, chat_id: int):
        sql_query = "select * from keys where chat_id = $1"
        logger.info(f'Student - {chat_id} check_tester')
        return await self.pool.fetch(sql_query, chat_id)

    async def check_captain(self, id_chat: int):
        sql_query = "select privilege from student where chat_id = $1"
        # logger.info('Student - {0} check_captain'.format(chat_id))
        return await self.pool.fetch(sql_query, id_chat)

    #########################
    #       GET ADMIN       #
    #########################
    async def admin_get_users_list(self, admin_id_chat: int) -> str:
        sql_query = "select chat_id, u_name, surname, group_id, privilege from student"
        logger.info(f'admin_get_users_list. Checks {admin_id_chat}')
        return await self.pool.fetch(sql_query)

    async def admin_get_user_bio(self, admin_id_chat: int, id_chat: int) -> str:
        sql_query = "select chat_id, u_name, surname, group_id, privilege, ban from student where chat_id = $1"
        logger.info(f'Student - {id_chat} admin_get_user. Checks {admin_id_chat}')
        return await self.pool.fetch(sql_query, id_chat)

    async def admin_get_users_classmates(self, id_chat: int) -> str:
        sql_query = "select chat_id, u_name, surname, group_id from student where group_id = (select group_id from " \
                    "student where chat_id = $1) "
        logger.info(f'admin_get_users_classmates. Checks {id_chat}')
        return await self.pool.fetch(sql_query, id_chat)

    #########################
    #          GET          #
    #########################

    async def get_whose_sched(self, id_chat: int):
        sql_query = "select whose_schedule from student where chat_id = $1"
        logger.info(f'Student - {id_chat} get_whose_sched')
        return await self.pool.fetch(sql_query, id_chat)

    async def get_user(self, id_chat: int) -> str:
        sql_query = "select * from student where chat_id = $1"
        logger.info(f'Student - {id_chat} get_user')
        return await self.pool.fetch(sql_query, id_chat)

    async def get_arhit_sched(self, id_chat: int):
        sql_query = 'select sched_arhit from groups_students where id=cast((select group_id from student where ' \
                    'chat_id = $1) as INT) '
        logger.info(f'Student - {id_chat} get_arhit_sched')
        return await self.pool.fetchrow(sql_query, id_chat)

    async def get_group_sched(self, id_chat: int):
        sql_query = 'select sched_group from groups_students where id=cast((select group_id from student where ' \
                    'chat_id = $1) as INT) '
        logger.info(f'Student - {id_chat} get_group_sched')
        return await self.pool.fetchrow(sql_query, id_chat)

    ####
    async def get_group_sched_by_group_id(self, group_id: int):
        sql_query = 'select sched_group from groups_students where id=$1'
        return await self.pool.fetchrow(sql_query, group_id)

    async def get_arhit_sched_by_group_id(self, group_id: int):
        sql_query = 'select sched_arhit from groups_students where id=$1'
        return await self.pool.fetchrow(sql_query, group_id)

    ####

    async def get_user_sched(self, id_chat: int):
        sql_query = 'select sched_user from student where chat_id = $1'
        logger.info(f'Student - {id_chat} get_user_sched')
        return await self.pool.fetchrow(sql_query, id_chat)

    async def get_group_name(self, id_inc: int) -> str:
        sql_query = "select group_name from groups_students where id = $1"
        return await self.pool.fetch(sql_query, id_inc)

    async def get_group_name_user(self, id_inc: int) -> str:
        sql_query = "select group_name from student where chat_id = $1"
        return await self.pool.fetch(sql_query, id_inc)

    async def get_group_id(self, group_name: str):
        sql_query = "select id from groups_students where group_name = $1"
        return await self.pool.fetchrow(sql_query, group_name)

    async def get_institution(self, id_inc: int):
        sql_query = 'select url from institution where id = $1'
        return await self.pool.fetch(sql_query, id_inc)

    async def get_institution_url_groups(self, id_inc: int):
        sql_query = 'select url_for_groups from institution where id = $1'
        return await self.pool.fetch(sql_query, id_inc)

    async def get_groups_values(self, institution_id: int):
        sql_query = 'select group_url_value, id from groups_students where institution_id = $1'
        return await self.pool.fetch(sql_query, institution_id)

    async def get_all_groups(self):
        sql_query = 'select group_name from groups_students'
        return await self.pool.fetch(sql_query)

    async def get_groups_name(self):
        sql_query = 'select group_name from groups_students'
        return await self.pool.fetch(sql_query)

    async def get_groups_sched_name_arhit(self, id_inc: int):
        sql_query = 'select group_name, sched_arhit from groups_students where id = $1'
        return await self.pool.fetch(sql_query, id_inc)

    async def get_groups_sched_name_group(self, id_inc: int):
        sql_query = 'select group_name, sched_group from groups_students where id = $1'
        return await self.pool.fetch(sql_query, id_inc)

    async def get_institution_ids(self):
        return await self.pool.fetch('select id from institution')

    async def get_free_hashes(self):
        return await self.pool.fetch('select key_md5 from keys where chat_id is null')

    #########################
    #          ADD          #
    #########################

    async def add_user(self, id_chat: int, name: str, surname: str, group_id: str, group_name: str):
        sql_query = "insert into student (chat_id, u_name, surname, group_id, group_name," \
                    " whose_schedule, ban, privilege)" \
                    " values ($1, $2, $3, $4, $5, \'general\', False, 0) "
        logger.info(f'Student - {id_chat} add_user')
        await self.pool.execute(sql_query, id_chat, name, surname, group_id, group_name)

    async def add_group(self, group_name: str, id_group: int, url_value: str):
        sql_query = 'insert into groups_students(group_name, institution_id, group_url_value) values ($1, $2, $3);'
        return await self.pool.execute(sql_query, group_name, id_group, url_value)

    async def add_institution(self, instit_name: str, url: str, url_for_groups: str):
        sql_query = 'insert into institution(instit_name, sched, url_for_groups) values ($1, $2, $3)'
        return await self.pool.execute(sql_query, instit_name, url, url_for_groups)

    async def add_key(self, hash: str, date: str):
        sql_query = 'insert into keys(key_md5, time_created) values ($1, $2)'
        return await self.pool.execute(sql_query, hash, date)

    async def add_photo(self, user_id: str, group_id: int, file_type: str, type_task, date_download, file_id):
        sql_query = 'insert into task(user_id, group_id, file_type, type_task, date_download, file_id) ' \
                    'values ($1, $2, $3, $4, $5, $6)'
        return await self.pool.execute(sql_query, user_id, group_id, file_type, type_task, date_download, file_id)

    #########################
    #        UPDATE         #
    #########################
    async def update_whose_schedule(self, whose: str, id_chat: int) -> str:
        sql_query = "update student set whose_schedule = $1 where chat_id = $2"
        logger.info(f'Student - {id_chat} update_whose_schedule, privilege - {whose}')
        return await self.pool.execute(sql_query, whose, id_chat)

    async def update_privilege(self, privilege: int, id_chat: int) -> str:
        sql_query = "update student set privilege = $1 where chat_id = $2"
        logger.info(f'Student - {id_chat} update_privilege, privilege - {privilege}')
        return await self.pool.execute(sql_query, privilege, id_chat)

    async def update_arhit_sched(self, sched: str, id_inc: int):
        sql_query = 'update groups_students set sched_arhit = $1 where id = $2;'
        return await self.pool.execute(sql_query, sched, id_inc)

    async def update_group_sched(self, sched: str, id_chat: int):
        sql_query = 'update groups_students set sched_group = $1 where id = cast((select group_id from student ' \
                    'where chat_id = $2) as INT) '
        return await self.pool.execute(sql_query, sched, id_chat)

    async def update_user_sched(self, sched: str, id_chat: int):
        sql_query = 'update student set sched_user = $1 where chat_id = $2;'
        return await self.pool.execute(sql_query, sched, id_chat)

    async def update_captain(self, id_chat: str, hash: str, date: str, group_name: str):
        sql_query = 'update keys set (chat_id, time_start_use, group_name) = ($1, $3, $4) where key_md5 = $2;'
        logger.info(f'Student - {id_chat} update_captain')
        return await self.pool.execute(sql_query, id_chat, hash, date, group_name)

    async def update_ban(self, admin_id_chat: int, id_chat: int, ban: bool):
        sql_query = 'update student set ban = $1 where chat_id = $2;'
        logger.info(f'Admin - {admin_id_chat} update_ban for user - {id_chat}, set - {ban}')
        return await self.pool.execute(sql_query, ban, id_chat)

    async def update_lock(self, id_chat: int, lock: bool):
        sql_query = 'update groups_students set lock = $1 where id = (select cast(group_id as int) from student ' \
                    'where chat_id = $2); '
        logger.info(f'Student - {id_chat} update_lock_group, set - {lock}')
        return await self.pool.execute(sql_query, lock, id_chat)

    #########################
    #          DEL          #
    #########################

    async def delete_account(self, id_chat: str):
        sql_query = 'delete from student where  chat_id = $1;'
        logger.info('Student - {0} delete_account'.format(id_chat))
        return await self.pool.execute(sql_query, id_chat)

    async def test_connect(self):
        return await self.pool.execute('select version();')

'''

import psycopg2
from configparser import ConfigParser


def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()
'''
