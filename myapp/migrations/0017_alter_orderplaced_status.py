# Generated by Django 5.0.6 on 2024-08-29 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_contactmessage_alter_orderplaced_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('Packed', 'Packed'), ('Pending', 'Pending'), ('On the Way', 'On The Way'), ('Accepted', 'Accepted'), ('Delivered', 'Delivered'), ('Cancel', 'Cancel')], default='pending', max_length=50),
        ),
    ]