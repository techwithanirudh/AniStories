# Generated by Django 2.1 on 2021-11-15 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='blog_pics'),
        ),
    ]
