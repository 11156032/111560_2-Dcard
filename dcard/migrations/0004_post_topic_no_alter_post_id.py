# Generated by Django 5.1 on 2024-11-13 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcard', '0003_auto_20241102_0707'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='topic_no',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
