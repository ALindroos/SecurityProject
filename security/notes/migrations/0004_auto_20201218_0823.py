# Generated by Django 3.1.4 on 2020-12-18 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0003_auto_20201216_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='note_text',
            field=models.TextField(max_length=200),
        ),
    ]
