# Generated by Django 3.0.3 on 2020-05-16 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miscosas', '0011_item_id_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='foto',
            field=models.ImageField(default='', upload_to='img_comens'),
        ),
    ]
