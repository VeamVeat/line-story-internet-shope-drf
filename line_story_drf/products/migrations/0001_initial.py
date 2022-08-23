# Generated by Django 4.1 on 2022-08-23 08:42

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255, verbose_name='type of file')),
                ('image', models.ImageField(upload_to=products.models.get_path_file, validators=[products.models.validate_image])),
                ('size', models.IntegerField(default=0, verbose_name='size of file')),
                ('name', models.CharField(max_length=255, verbose_name='name of file')),
            ],
            options={
                'verbose_name': 'file',
                'verbose_name_plural': 'files',
            },
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name of product')),
            ],
            options={
                'verbose_name': 'type of product',
                'verbose_name_plural': 'type of products',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(unique=True)),
                ('title', models.CharField(max_length=255, verbose_name='name of product')),
                ('description', models.TextField(verbose_name='name of description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='price of product')),
                ('year', models.IntegerField(db_index=True, verbose_name='year of product release')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='number of products')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to='products.producttype')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
            },
        ),
        migrations.CreateModel(
            name='ProductFile',
            fields=[
                ('file_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.file')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_file', to='products.product')),
            ],
            bases=('products.file',),
        ),
    ]
