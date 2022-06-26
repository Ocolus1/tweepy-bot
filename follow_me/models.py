import json
from tabnanny import check
from django.db import models
from django.utils import timezone
from django_enum_choices.fields import EnumChoiceField
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from .enums import TimeInterval, SetupStatus
from django.contrib.auth.models import (
    BaseUserManager
)
from django.contrib.auth.models import AbstractUser
import string
from random import choices

class MyUserManager(BaseUserManager):
    def create_user(self, twitter_id, name, password=None):

        user = self.model(
            twitter_id=twitter_id,
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, twitter_id, name, password=None):
        """
        Creates and saves a superuser id and password.
        """
        user = self.create_user(
            twitter_id,
            name,
            password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user



class User(AbstractUser):
    username = None
    twitter_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=500, blank=True, null=True)
    screen_name = models.CharField(max_length=500, blank=True, null=True)
    gen_c = models.CharField(max_length=150, blank=True, null=True)
    num_of_followers = models.IntegerField( blank=True, null=True)
    status = EnumChoiceField(SetupStatus, default=SetupStatus.disabled)
    message = models.TextField()
    prev_message = models.TextField()
    # time_interval = EnumChoiceField(TimeInterval, default=TimeInterval.thirty_sec)
    access_token = models.CharField(max_length=500, blank=True, null=True)
    access_token_secret = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField('timestamp', auto_now_add=True, editable=False,
                            db_index=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    task = models.OneToOneField(
        PeriodicTask,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    check_task = models.OneToOneField(
        PeriodicTask,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="check_task"
    )

    objects = MyUserManager()

    USERNAME_FIELD = 'twitter_id'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    def delete(self, *args, **kwargs):
        if self.task is not None:
            self.task.delete()
        return super(User, self).delete(*args, **kwargs)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    def setup_task(self):
        self.task = PeriodicTask.objects.create(
            name=self.twitter_id,
            task='computation_heavy_task',
            interval=self.interval_schedule,
            args=json.dumps([self.id]),
            start_time=timezone.now(),
            enabled=False
        )
        self.check_task = PeriodicTask.objects.create(
            name=str(self.id) + self.generate_rand_text(),
            task='check_20_min',
            interval=self.check_interval_schedule,
            args=json.dumps([self.id]),
            start_time=timezone.now(),
            enabled=False
        )
        self.save()

    def generate_rand_text(self):
        characters = string.digits + string.ascii_letters
        gen_c = "".join(choices(characters, k=10))

        return gen_c

    @property
    def check_interval_schedule(self):
        schedule, created = IntervalSchedule.objects.get_or_create(every=20, period=IntervalSchedule.MINUTES)
        return schedule

    @property
    def interval_schedule(self):
        schedule, created = IntervalSchedule.objects.get_or_create(every=1, period=IntervalSchedule.MINUTES)
        return schedule



class User_list(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "user_follower")
    follower = models.BigIntegerField()

