# Generated by Django 5.0.3 on 2024-04-05 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_sale_curierinvoice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='curierInvoice',
        ),
        migrations.AddField(
            model_name='customer',
            name='courierInvoice',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]