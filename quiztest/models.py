from django.db import models


class Login(models.Model):
    user_id = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    difficulty = models.CharField(max_length=10)

    class Meta:
        db_table = 'login_details'
