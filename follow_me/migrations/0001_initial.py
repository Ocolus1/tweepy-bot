# Generated by Django 3.2.13 on 2022-06-06 17:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_enum_choices.choice_builders
import django_enum_choices.fields
import follow_me.enums


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_celery_beat', '0015_edit_solarschedule_events_choices'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('twitter_id', models.BigIntegerField(unique=True)),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('screen_name', models.CharField(blank=True, max_length=500, null=True)),
                ('gen_c', models.CharField(blank=True, max_length=150, null=True)),
                ('num_of_followers', models.IntegerField(blank=True, null=True)),
                ('status', django_enum_choices.fields.EnumChoiceField(choice_builder=django_enum_choices.choice_builders.value_value, choices=[('Active', 'Active'), ('Disabled', 'Disabled')], default=follow_me.enums.SetupStatus['disabled'], enum_class=follow_me.enums.SetupStatus, max_length=8)),
                ('access_token', models.CharField(blank=True, max_length=500, null=True)),
                ('access_token_secret', models.CharField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='timestamp')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('check_task', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='check_task', to='django_celery_beat.periodictask')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('task', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='django_celery_beat.periodictask')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.BigIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_follower', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
