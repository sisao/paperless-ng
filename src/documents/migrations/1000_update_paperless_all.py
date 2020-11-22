# Generated by Django 3.1.3 on 2020-11-07 12:35
import uuid

from django.db import migrations, models
import django.db.models.deletion


def make_index(apps, schema_editor):
    Document = apps.get_model("documents", "Document")
    documents = Document.objects.all()
    print()
    try:
        print("  --> Creating document index...")
        from whoosh.writing import AsyncWriter
        from documents import index
        ix = index.open_index(recreate=True)
        with AsyncWriter(ix) as writer:
            for document in documents:
                index.update_document(writer, document)
    except ImportError:
        # index may not be relevant anymore
        print("  --> Cannot create document index.")


def logs_set_default_group(apps, schema_editor):
    Log = apps.get_model('documents', 'Log')
    for log in Log.objects.all():
        if log.group is None:
            log.group = uuid.uuid4()
            log.save()


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0023_document_current_filename'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='archive_serial_number',
            field=models.IntegerField(blank=True, db_index=True, help_text='The position of this document in your physical document archive.', null=True, unique=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='is_inbox_tag',
            field=models.BooleanField(default=False, help_text='Marks this tag as an inbox tag: All newly consumed documents will be tagged with inbox tags.'),
        ),
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('slug', models.SlugField(blank=True, editable=False)),
                ('match', models.CharField(blank=True, max_length=256)),
                ('matching_algorithm', models.PositiveIntegerField(choices=[(1, 'Any'), (2, 'All'), (3, 'Literal'), (4, 'Regular Expression'), (5, 'Fuzzy Match'), (6, 'Automatic Classification')], default=1, help_text='Which algorithm you want to use when matching text to the OCR\'d PDF.  Here, "any" looks for any occurrence of any word provided in the PDF, while "all" requires that every word provided appear in the PDF, albeit not in the order provided.  A "literal" match means that the text you enter must appear in the PDF exactly as you\'ve entered it, and "regular expression" uses a regex to match the PDF.  (If you don\'t know what a regex is, you probably don\'t want this option.)  Finally, a "fuzzy match" looks for words or phrases that are mostly—but not exactly—the same, which can be useful for matching against documents containg imperfections that foil accurate OCR.')),
                ('is_insensitive', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='document',
            name='document_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='documents', to='documents.documenttype'),
        ),
        migrations.AlterField(
            model_name='correspondent',
            name='matching_algorithm',
            field=models.PositiveIntegerField(choices=[(1, 'Any'), (2, 'All'), (3, 'Literal'), (4, 'Regular Expression'), (5, 'Fuzzy Match'), (6, 'Automatic Classification')], default=1, help_text='Which algorithm you want to use when matching text to the OCR\'d PDF.  Here, "any" looks for any occurrence of any word provided in the PDF, while "all" requires that every word provided appear in the PDF, albeit not in the order provided.  A "literal" match means that the text you enter must appear in the PDF exactly as you\'ve entered it, and "regular expression" uses a regex to match the PDF.  (If you don\'t know what a regex is, you probably don\'t want this option.)  Finally, a "fuzzy match" looks for words or phrases that are mostly—but not exactly—the same, which can be useful for matching against documents containg imperfections that foil accurate OCR.'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='matching_algorithm',
            field=models.PositiveIntegerField(choices=[(1, 'Any'), (2, 'All'), (3, 'Literal'), (4, 'Regular Expression'), (5, 'Fuzzy Match'), (6, 'Automatic Classification')], default=1, help_text='Which algorithm you want to use when matching text to the OCR\'d PDF.  Here, "any" looks for any occurrence of any word provided in the PDF, while "all" requires that every word provided appear in the PDF, albeit not in the order provided.  A "literal" match means that the text you enter must appear in the PDF exactly as you\'ve entered it, and "regular expression" uses a regex to match the PDF.  (If you don\'t know what a regex is, you probably don\'t want this option.)  Finally, a "fuzzy match" looks for words or phrases that are mostly—but not exactly—the same, which can be useful for matching against documents containg imperfections that foil accurate OCR.'),
        ),
        migrations.AlterField(
            model_name='document',
            name='content',
            field=models.TextField(blank=True, help_text='The raw, text-only data of the document. This field is primarily used for searching.'),
        ),
        migrations.AlterModelOptions(
            name='log',
            options={'ordering': ('-created',)},
        ),
        migrations.RemoveField(
            model_name='log',
            name='modified',
        ),
        migrations.AlterField(
            model_name='log',
            name='group',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.RunPython(
            code=django.db.migrations.operations.special.RunPython.noop,
            reverse_code=logs_set_default_group
        ),
        migrations.RunPython(
            code=make_index,
            reverse_code=django.db.migrations.operations.special.RunPython.noop,
        ),
    ]
