# Generated by Django 5.2 on 2025-05-12 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_borrowbook_actual_return_date_borrowbook_is_returned'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='total_copies',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
