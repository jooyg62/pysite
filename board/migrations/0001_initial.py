# Generated by Django 2.2.2 on 2019-06-21 05:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('contents', models.TextField()),
                ('hit', models.CharField(default=0, max_length=20)),
                ('reg_date', models.DateTimeField(auto_now=True)),
                ('group_no', models.CharField(max_length=20)),
                ('order_no', models.CharField(max_length=20)),
                ('depth', models.CharField(max_length=20)),
                ('img_ori_name', models.CharField(max_length=200)),
                ('img_url', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
        ),
    ]
