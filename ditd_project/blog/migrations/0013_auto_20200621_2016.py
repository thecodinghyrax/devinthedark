# Generated by Django 3.0.7 on 2020-06-21 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20200621_2006'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='icon',
            field=models.CharField(default='change me', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='topic',
            name='topic',
            field=models.CharField(max_length=30),
        ),
    ]
