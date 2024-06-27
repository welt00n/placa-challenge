from django.db.models import Model as BaseModel
from django.db.models import IntegerField, CharField, BooleanField, DateTimeField

class Interviewee(BaseModel):
    name = CharField(max_length=50, default="")
    years_of_experience = IntegerField()
    favorite_programming_language = CharField(max_length=50, default="")
    interview_date = CharField(max_length=50, default="")
    willing_to_work_onsite = BooleanField()
    willing_to_use_ruby = BooleanField()
    created_at = DateTimeField()

    def summary(self):
        return f"Name: {self.name}, years_of_experience: {self.years_of_experience}, favorite prograaming language: {self.favorite_programming_language}"
    def __str__(self):
        return self.name