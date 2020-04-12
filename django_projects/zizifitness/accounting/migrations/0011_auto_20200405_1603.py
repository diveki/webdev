# Generated by Django 3.0.4 on 2020-04-05 14:03

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounting', '0010_auto_20200405_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenseitems',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 4, 5, 14, 3, 4, 288221, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='incomeitems',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 4, 5, 14, 3, 4, 287223, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='salary',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 4, 5, 14, 3, 4, 289217, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='salarydistribution',
            name='instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='salarydistribution',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.IncomeCategories'),
        ),
    ]