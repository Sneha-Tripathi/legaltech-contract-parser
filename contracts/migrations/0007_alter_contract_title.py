

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0006_contract_extracted_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
