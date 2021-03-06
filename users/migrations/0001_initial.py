# Generated by Django 3.2.5 on 2022-01-11 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('kakao_id', models.CharField(max_length=25, unique=True)),
                ('nickname', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=30)),
                ('gender', models.IntegerField()),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
