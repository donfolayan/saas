# Generated by Django 5.1.7 on 2025-04-25 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0017_subscription_subtitle'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersubscription',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
