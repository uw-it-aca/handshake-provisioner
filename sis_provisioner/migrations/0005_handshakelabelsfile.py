# Generated by Django 4.2.7 on 2023-11-29 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sis_provisioner', '0004_blockedhandshakestudent'),
    ]

    operations = [
        migrations.CreateModel(
            name='HandshakeLabelsFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_test_file', models.BooleanField(default=False)),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sis_provisioner.term')),
            ],
        ),
    ]
