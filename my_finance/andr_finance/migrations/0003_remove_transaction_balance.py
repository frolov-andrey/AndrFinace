# Generated by Django 4.1.13 on 2024-04-01 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('andr_finance', '0002_alter_transaction_type_transaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='balance',
        ),
    ]