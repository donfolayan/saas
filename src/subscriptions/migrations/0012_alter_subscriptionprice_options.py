# Generated by Django 5.1.7 on 2025-03-31 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0011_subscriptionprice_timestamp_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscriptionprice',
            options={'ordering': ['order', 'featured', '-updated']},
        ),
    ]
