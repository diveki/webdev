# Generated by Django 3.0.4 on 2020-03-28 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IncomeCategories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a category type', max_length=200)),
                ('unit_price', models.FloatField(null=True)),
                ('category_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.CategoryType')),
            ],
        ),
    ]
