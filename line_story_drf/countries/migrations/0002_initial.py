from django.db import migrations

from utils.list_countries import countries


def forwards_add_counries(apps, schema_editor):
    Country = apps.get_model("countries", "Country")

    objects_country = []

    for dict_country in countries:
        values = list(dict_country.values())
        objects_country.append(Country(name=values[0], reduction=values[1]))
    Country.objects.bulk_create(objects_country)


def reset_delete_table(apps, schema_editor):
    Country = apps.get_model("countries", "Country")

    Country.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('countries', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_add_counries, reset_delete_table),
    ]
