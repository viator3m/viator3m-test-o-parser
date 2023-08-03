# Generated by Django 3.2.20 on 2023-08-02 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parsing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_field', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('price', models.IntegerField()),
                ('link', models.URLField(max_length=512)),
                ('parser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='parser.parsing')),
            ],
        ),
    ]
