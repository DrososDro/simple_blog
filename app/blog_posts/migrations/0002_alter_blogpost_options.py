# Generated by Django 4.2.3 on 2023-10-30 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpost',
            options={'ordering': ['-created_at']},
        ),
    ]
