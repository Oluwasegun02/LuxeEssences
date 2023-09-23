# Generated by Django 4.2.4 on 2023-09-12 17:13

from django.db import migrations, models
import store.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=150)),
                ('name', models.CharField(max_length=150)),
                ('image', models.ImageField(blank=True, null=True, upload_to=store.models.get_file_path)),
                ('description', models.TextField(max_length=500)),
                ('status', models.BooleanField(default=False, help_text='0-default, 1-Hidden')),
                ('trending', models.BooleanField(default=False, help_text='0-default, 1-trending')),
                ('meta_title', models.CharField(max_length=150)),
                ('meta_keyworlds', models.CharField(max_length=150)),
                ('meta_description', models.TextField(max_length=500)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
