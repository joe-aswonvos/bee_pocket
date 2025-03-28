# Generated by Django 5.1.6 on 2025-03-12 09:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admin_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Repeatability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RepeatableDaily', models.BooleanField(default=False)),
                ('WeeklyRepeatInterval', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Weekday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=50)),
                ('item_description', models.CharField(max_length=200)),
                ('item_type', models.CharField(choices=[('Task', 'Pollen'), ('Consequence', 'Sting'), ('Reward', 'Honey'), ('Adjustment', 'Adjustment')], max_length=20)),
                ('item_value', models.IntegerField()),
                ('createdon', models.DateTimeField(auto_now_add=True)),
                ('repeatability', models.BooleanField(default=False)),
                ('createdby', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('item_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pocket_app.category')),
                ('repeatID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pocket_app.repeatability')),
            ],
        ),
        migrations.CreateModel(
            name='ItemInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Lasteditedon', models.DateTimeField(auto_now=True)),
                ('CreatedOn', models.DateTimeField(auto_now_add=True)),
                ('expireon', models.DateTimeField()),
                ('ActiveStatus', models.BooleanField(default=True)),
                ('Approved', models.BooleanField(default=False)),
                ('ApprovedBy', models.CharField(blank=True, max_length=255, null=True)),
                ('ApprovedOn', models.DateTimeField(blank=True, null=True)),
                ('BeePocketID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.beepocket')),
                ('CreatedBy', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_items', to=settings.AUTH_USER_MODEL)),
                ('Lasteditedby', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='last_edited_items', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pocket_app.item')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Comment', models.CharField(max_length=500)),
                ('CreatedOn', models.DateTimeField(auto_now_add=True)),
                ('CreatedBy', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('ItemInstance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pocket_app.iteminstance')),
            ],
        ),
        migrations.AddField(
            model_name='repeatability',
            name='RepeatableWeekly',
            field=models.ManyToManyField(blank=True, to='pocket_app.weekday'),
        ),
    ]
