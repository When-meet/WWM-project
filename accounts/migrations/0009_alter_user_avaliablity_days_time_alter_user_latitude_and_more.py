# Generated by Django 4.1 on 2022-10-25 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avaliablity_days_time',
            field=models.TextField(blank=True, default='000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000', verbose_name='meet 가능 시간'),
        ),
        migrations.AlterField(
            model_name='user',
            name='latitude',
            field=models.FloatField(default=0, null=True, verbose_name='위도'),
        ),
        migrations.AlterField(
            model_name='user',
            name='longitude',
            field=models.FloatField(default=0, null=True, verbose_name='경도'),
        ),
    ]
