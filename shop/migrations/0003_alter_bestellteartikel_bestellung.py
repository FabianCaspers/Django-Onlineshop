# Generated by Django 4.2.3 on 2023-07-20 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_artikel_bild'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bestellteartikel',
            name='bestellung',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bestellteartikel', to='shop.bestellung'),
        ),
    ]