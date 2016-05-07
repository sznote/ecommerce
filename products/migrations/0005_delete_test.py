# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_test'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Test',
        ),
    ]
