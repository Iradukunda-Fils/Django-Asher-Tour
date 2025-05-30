# Generated by Django 5.1.3 on 2025-05-09 22:55

import django.core.validators
import django.db.models.deletion
import django_countries.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['name'], name='system_db_c_name_4606fe_idx')],
            },
        ),
        migrations.CreateModel(
            name='TourPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='package_profile/')),
                ('title', models.CharField(db_index=True, max_length=255, unique=True)),
                ('deadline', models.DateField(db_index=True)),
                ('group_size', models.PositiveIntegerField(help_text='Minimum group size is 1', validators=[django.core.validators.MinValueValidator(1)])),
                ('location', django_countries.fields.CountryField(default='RW', max_length=2)),
                ('description', models.TextField(max_length=500)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('is_published', models.BooleanField(db_index=True, default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='packages', to='system_db.category')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_packages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Tour Package',
                'verbose_name_plural': 'Tour Packages',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(help_text='Rating must be between 1 and 5', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL)),
                ('replay', models.ForeignKey(blank=True, help_text='Reference to another review this is a reply to', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='system_db.review')),
                ('tour_package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='system_db.tourpackage')),
            ],
            options={
                'verbose_name': 'Review',
                'verbose_name_plural': 'Reviews',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PackageOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=255, unique=True)),
                ('description', models.TextField(blank=True, max_length=100)),
                ('discount_price', models.DecimalField(blank=True, db_index=True, decimal_places=2, help_text='Discounted price of the tour package', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('start_date', models.DateTimeField(db_index=True)),
                ('end_date', models.DateTimeField(db_index=True)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('tour_package', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='offers', to='system_db.tourpackage')),
            ],
            options={
                'verbose_name': 'Package Offer',
                'verbose_name_plural': 'Package Offers',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PackageMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(help_text='List of images', upload_to='package_images')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tour_package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media', to='system_db.tourpackage')),
            ],
            options={
                'verbose_name': 'Package Media',
                'verbose_name_plural': 'Package Media',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Itinerary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=255)),
                ('day_number', models.PositiveIntegerField(db_index=True)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('tour_package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itineraries', to='system_db.tourpackage')),
            ],
            options={
                'verbose_name': 'Itinerary',
                'verbose_name_plural': 'Itineraries',
                'ordering': ['day_number'],
            },
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='destinations')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('description', models.TextField(blank=True)),
                ('location', models.CharField(db_index=True, max_length=255)),
                ('is_popular', models.BooleanField(db_index=True, default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('tour_package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destinations', to='system_db.tourpackage')),
            ],
            options={
                'verbose_name': 'Destination',
                'verbose_name_plural': 'Destinations',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='tourpackage',
            index=models.Index(fields=['is_active', 'is_published'], name='system_db_t_is_acti_d237cb_idx'),
        ),
        migrations.AddIndex(
            model_name='tourpackage',
            index=models.Index(fields=['deadline'], name='system_db_t_deadlin_c4ab9b_idx'),
        ),
        migrations.AddConstraint(
            model_name='tourpackage',
            constraint=models.CheckConstraint(condition=models.Q(('price__gte', 0)), name='price_non_negative'),
        ),
        migrations.AddConstraint(
            model_name='tourpackage',
            constraint=models.CheckConstraint(condition=models.Q(('group_size__gte', 1)), name='group_size_min_one'),
        ),
        migrations.AddIndex(
            model_name='review',
            index=models.Index(fields=['tour_package', 'customer'], name='system_db_r_tour_pa_e927f0_idx'),
        ),
        migrations.AddIndex(
            model_name='packageoffer',
            index=models.Index(fields=['is_active', 'start_date', 'end_date'], name='system_db_p_is_acti_39c7b8_idx'),
        ),
        migrations.AddConstraint(
            model_name='packageoffer',
            constraint=models.CheckConstraint(condition=models.Q(('discount_price__gte', 0)), name='discount_price_non_negative'),
        ),
        migrations.AddIndex(
            model_name='packagemedia',
            index=models.Index(fields=['tour_package'], name='system_db_p_tour_pa_c213eb_idx'),
        ),
        migrations.AddIndex(
            model_name='itinerary',
            index=models.Index(fields=['tour_package', 'day_number'], name='system_db_i_tour_pa_4ca1ee_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='itinerary',
            unique_together={('tour_package', 'day_number')},
        ),
        migrations.AddIndex(
            model_name='destination',
            index=models.Index(fields=['tour_package', 'name'], name='system_db_d_tour_pa_0e2aa7_idx'),
        ),
        migrations.AddIndex(
            model_name='destination',
            index=models.Index(fields=['is_popular'], name='system_db_d_is_popu_844305_idx'),
        ),
    ]
