# Generated by Django 4.2.4 on 2023-10-02 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default='Menunggu Konfirmasi', max_length=100),
        ),
    ]