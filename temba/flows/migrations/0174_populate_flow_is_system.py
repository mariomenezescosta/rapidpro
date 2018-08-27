# Generated by Django 2.0.8 on 2018-08-27 19:48

from django.db import migrations

from temba.utils import chunk_list


def populate_is_system(apps, schema_editor):
    Flow = apps.get_model("flows", "Flow")

    total = Flow.objects.filter().count()
    if total:
        print(f"Updating is_system on {total} flows...")

    num_updated = 0

    for batch in chunk_list(Flow.objects.exclude(flow_type="M"), 1000):
        Flow.objects.filter(id__in=[f.id for f in batch]).update(is_system=False)

        num_updated += len(batch)
        print(f" > Updated {num_updated} of {total} flows")

    for batch in chunk_list(Flow.objects.filter(flow_type="M"), 1000):
        Flow.objects.filter(id__in=[f.id for f in batch]).update(is_system=True)

        num_updated += len(batch)
        print(f" > Updated {num_updated} of {total} flows")


class Migration(migrations.Migration):

    dependencies = [("flows", "0173_flow_is_system")]

    operations = [migrations.RunPython(populate_is_system)]
