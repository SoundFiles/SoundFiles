# Generated by Django 3.1.5 on 2021-04-20 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userfeatures', '0020_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='sub_type',
            field=models.CharField(default='podcast', max_length=25),
            preserve_default=False,
        ),
    ]