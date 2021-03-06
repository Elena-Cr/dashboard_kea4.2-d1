# Generated by Django 4.0.3 on 2022-03-24 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.BigIntegerField(blank=True, null=True)),
                ('customer_id', models.BigIntegerField(blank=True, null=True)),
                ('first_name', models.TextField(blank=True, null=True)),
                ('last_name', models.TextField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('postcode', models.BigIntegerField(blank=True, null=True)),
                ('city', models.TextField(blank=True, null=True)),
                ('country', models.TextField(blank=True, null=True)),
                ('ascii_safe_email', models.TextField(blank=True, null=True)),
                ('date_of_birth', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'customers',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.BigIntegerField(blank=True, null=True)),
                ('employee_id', models.BigIntegerField(blank=True, null=True)),
                ('firstname', models.TextField(blank=True, null=True)),
                ('lastname', models.TextField(blank=True, null=True)),
                ('date_of_birth', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'employees',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Geodata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.BigIntegerField(blank=True, null=True)),
                ('country', models.TextField(blank=True, null=True)),
                ('lat', models.TextField(blank=True, null=True)),
                ('lon', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'geodata',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.BigIntegerField(blank=True, null=True)),
                ('order_id', models.BigIntegerField(blank=True, null=True)),
                ('product_id', models.BigIntegerField(blank=True, null=True)),
                ('unitprice', models.FloatField(blank=True, null=True)),
                ('quantity', models.BigIntegerField(blank=True, null=True)),
                ('customer_id', models.BigIntegerField(blank=True, null=True)),
                ('orderdate', models.DateTimeField(blank=True, null=True)),
                ('employee_id', models.BigIntegerField(blank=True, null=True)),
                ('deliverydate', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'orders',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.BigIntegerField(blank=True, null=True)),
                ('product_id', models.BigIntegerField(blank=True, null=True)),
                ('productname', models.TextField(blank=True, null=True)),
                ('stock', models.BigIntegerField(blank=True, null=True)),
                ('reorder', models.BigIntegerField(blank=True, null=True)),
                ('type', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'products',
                'managed': False,
            },
        ),
    ]
