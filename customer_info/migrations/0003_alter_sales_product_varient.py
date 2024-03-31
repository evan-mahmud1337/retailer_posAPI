# Generated by Django 4.1.7 on 2024-03-30 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
        ('customer_info', '0002_alter_sales_product_varient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales',
            name='product_varient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.varient'),
        ),
    ]