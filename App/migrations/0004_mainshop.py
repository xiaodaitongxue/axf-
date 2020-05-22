# Generated by Django 3.0.5 on 2020-04-28 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_mainmustbuy'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainShop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=128)),
                ('trackid', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'axf_shop',
            },
        ),
    ]
