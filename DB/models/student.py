from aiogram import types
from aiogram.utils.markdown import hlink
from tortoise import fields
from tortoise.models import Model

from DB.models.group import Group


async def get_all_students_name_id(msg: types.Message) -> dict:
    group_id = await Student.filter(chat_id=msg.chat.id).values_list('group_id')
    group_id = group_id[0][0]
    students = await Student.filter(group=group_id).values_list('id', 'name')
    result = {}
    for stud_id, stud_name in students:
        result.update({stud_id: stud_name})
    return result


async def get_student_id(msg: types.Message) -> int:
    stud_id = await Student.filter(chat_id=msg.chat.id).values_list('id')
    stud_id = stud_id[0][0]
    return stud_id


class Student(Model):
    id = fields.IntField(pk=True)
    chat_id = fields.BigIntField(unique=True)
    name = fields.CharField(max_length=64)
    surname = fields.CharField(max_length=64)
    patronymic = fields.CharField(max_length=64, null=True)
    group: fields.ForeignKeyRelation[Group] = fields.ForeignKeyField(
        "models.Group", related_name="group"
    )
    group_name = fields.CharField(max_length=32)
    sched_parts = fields.CharField(max_length=10, null=True)
    privilege = fields.CharField(max_length=1)
    sched_user = fields.TextField(null=True)
    whose_schedule = fields.CharField(max_length=1)
    ban = fields.BooleanField()

    subject: fields.ReverseRelation["models.subject.Subject"]

    class Meta:
        table = "student"

    @classmethod
    async def create_new_user(cls, user: types.User):
        user = await cls.create(
            tg_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            is_bot=user.is_bot
        )

        return user

    @property
    def mention_link(self):
        return hlink(self.fullname, f"tg://user?id={self.chat_id}")

    @property
    def fullname(self):
        if self.name is not None:
            return ' '.join((self.name, self.surname))

    # def __str__(self):
    #     return f"Student ID {self.chat_id}, by name {self.u_name} {self.s_name}"

    # def __repr__(self):
    #     return str(self)
