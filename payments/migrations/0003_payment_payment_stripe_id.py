# Generated by Django 4.2.5 on 2023-10-24 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_stripe_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='id платежа'),
        ),
    ]
