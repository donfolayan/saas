# Generated by Django 5.1.7 on 2025-03-29 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0006_usersubscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='stripe_product_id',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
