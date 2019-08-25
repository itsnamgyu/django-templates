# Generated by Django 2.2.3 on 2019-08-24 23:36

from django.db import migrations, models
import django.db.models.deletion
import versatileimagefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('identifier', models.CharField(max_length=256, verbose_name='identifier')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('title', models.CharField(blank=True, max_length=256, null=True, verbose_name='title')),
                ('image', versatileimagefield.fields.VersatileImageField(height_field='height', upload_to='carousel_image', verbose_name='image', width_field='width')),
                ('height', models.PositiveIntegerField(blank=True, null=True, verbose_name='image height')),
                ('width', models.PositiveIntegerField(blank=True, null=True, verbose_name='image width')),
                ('ppoi', versatileimagefield.fields.PPOIField(default='0.5x0.5', editable=False, max_length=20, verbose_name='image PPOI')),
            ],
        ),
        migrations.CreateModel(
            name='Placement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('carousel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='placements', to='carousel.Carousel')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carousel.Image')),
            ],
        ),
    ]
