# Generated by Django 5.0.4 on 2024-05-05 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videototext', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivo',
            name='archivo',
            field=models.FileField(upload_to='videototext/'),
        ),
    ]
