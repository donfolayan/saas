# Generated by Django 5.1.7 on 2025-04-06 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0015_subscriptionprice_features'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='features',
            field=models.TextField(blank=True, help_text='Comma separated list of features', null=True),
        ),
    ]
