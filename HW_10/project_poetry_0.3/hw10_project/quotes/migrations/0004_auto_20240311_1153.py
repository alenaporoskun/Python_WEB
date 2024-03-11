from django.db import migrations
from django.utils.text import slugify

def populate_slug_field(apps, schema_editor):
    Author = apps.get_model('quotes', 'Author')
    for author in Author.objects.all():
        author.slug = slugify(author.fullname)
        author.save()

class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0002_author_slug'),  # Попередня міграція, яку ви створили
    ]

    operations = [
        migrations.RunPython(populate_slug_field),
    ]
