# Generated by Django 5.0.4 on 2024-05-13 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videototext', '0008_alter_keywords_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivo',
            name='archivo',
            field=models.FileField(upload_to='media/files'),
        ),
    ]
