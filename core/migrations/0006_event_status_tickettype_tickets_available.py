# Generated by Django 4.2.8 on 2024-01-08 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_event_ticket_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='status',
            field=models.CharField(choices=[('expired', 'organizer'), ('available', 'available')], default='expired', max_length=50),
        ),
        migrations.AddField(
            model_name='tickettype',
            name='tickets_available',
            field=models.PositiveIntegerField(default=0),
        ),
    ]