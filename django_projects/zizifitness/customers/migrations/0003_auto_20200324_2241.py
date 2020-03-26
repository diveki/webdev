# Generated by Django 3.0.4 on 2020-03-24 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_auto_20200324_2221'),
    ]

    operations = [
        migrations.AddField(
            model_name='physical_appearance',
            name='biceps',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='physical_appearance',
            name='chest',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='physical_appearance',
            name='hip',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='physical_appearance',
            name='tigh',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='physical_appearance',
            name='date',
            field=models.DateField(),
        ),
    ]