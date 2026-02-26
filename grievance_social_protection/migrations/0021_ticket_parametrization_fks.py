import core.fields
import datetime
import uuid
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grievance_social_protection', '0020_ticketattachmenttype_alter_historicalticket_status_and_more'),
    ]

    operations = [
        # ── 1. Create lookup tables ──────────────────────────────────────────
        migrations.CreateModel(
            name='TicketCategory',
            fields=[
                ('validity_from', core.fields.DateTimeField(db_column='ValidityFrom', default=datetime.datetime.now)),
                ('validity_to', core.fields.DateTimeField(blank=True, db_column='ValidityTo', null=True)),
                ('legacy_id', models.IntegerField(blank=True, db_column='LegacyID', null=True)),
                ('id', models.AutoField(db_column='TicketCategoryID', primary_key=True, serialize=False)),
                ('uuid', models.CharField(db_column='TicketCategoryUUID', default=uuid.uuid4, max_length=36, unique=True)),
                ('codigo', models.CharField(db_column='Codigo', max_length=50)),
                ('nome', models.CharField(db_column='Nome', max_length=255)),
                ('descricao', models.CharField(blank=True, db_column='Descricao', max_length=500, null=True)),
                ('ativo', models.BooleanField(db_column='Ativo', default=True)),
            ],
            options={
                'db_table': 'tblTicketCategory',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TicketChannel',
            fields=[
                ('validity_from', core.fields.DateTimeField(db_column='ValidityFrom', default=datetime.datetime.now)),
                ('validity_to', core.fields.DateTimeField(blank=True, db_column='ValidityTo', null=True)),
                ('legacy_id', models.IntegerField(blank=True, db_column='LegacyID', null=True)),
                ('id', models.AutoField(db_column='TicketChannelID', primary_key=True, serialize=False)),
                ('uuid', models.CharField(db_column='TicketChannelUUID', default=uuid.uuid4, max_length=36, unique=True)),
                ('codigo', models.CharField(db_column='Codigo', max_length=50)),
                ('nome', models.CharField(db_column='Nome', max_length=255)),
                ('descricao', models.CharField(blank=True, db_column='Descricao', max_length=500, null=True)),
                ('ativo', models.BooleanField(db_column='Ativo', default=True)),
            ],
            options={
                'db_table': 'tblTicketChannel',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TicketFlag',
            fields=[
                ('validity_from', core.fields.DateTimeField(db_column='ValidityFrom', default=datetime.datetime.now)),
                ('validity_to', core.fields.DateTimeField(blank=True, db_column='ValidityTo', null=True)),
                ('legacy_id', models.IntegerField(blank=True, db_column='LegacyID', null=True)),
                ('id', models.AutoField(db_column='TicketFlagID', primary_key=True, serialize=False)),
                ('uuid', models.CharField(db_column='TicketFlagUUID', default=uuid.uuid4, max_length=36, unique=True)),
                ('codigo', models.CharField(db_column='Codigo', max_length=50)),
                ('nome', models.CharField(db_column='Nome', max_length=255)),
                ('descricao', models.CharField(blank=True, db_column='Descricao', max_length=500, null=True)),
                ('ativo', models.BooleanField(db_column='Ativo', default=True)),
            ],
            options={
                'db_table': 'tblTicketFlag',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TicketPriority',
            fields=[
                ('validity_from', core.fields.DateTimeField(db_column='ValidityFrom', default=datetime.datetime.now)),
                ('validity_to', core.fields.DateTimeField(blank=True, db_column='ValidityTo', null=True)),
                ('legacy_id', models.IntegerField(blank=True, db_column='LegacyID', null=True)),
                ('id', models.AutoField(db_column='TicketPriorityID', primary_key=True, serialize=False)),
                ('uuid', models.CharField(db_column='TicketPriorityUUID', default=uuid.uuid4, max_length=36, unique=True)),
                ('codigo', models.CharField(db_column='Codigo', max_length=50)),
                ('nome', models.CharField(db_column='Nome', max_length=255)),
                ('ordem', models.IntegerField(db_column='Ordem', default=0)),
                ('ativo', models.BooleanField(db_column='Ativo', default=True)),
            ],
            options={
                'db_table': 'tblTicketPriority',
                'managed': True,
            },
        ),

        # ── 2. Remove old CharField fields from ticket ───────────────────────
        migrations.RemoveField(model_name='ticket', name='category'),
        migrations.RemoveField(model_name='ticket', name='flags'),
        migrations.RemoveField(model_name='ticket', name='channel'),
        migrations.RemoveField(model_name='ticket', name='priority'),

        # ── 3. Remove old CharField fields from historicalticket ─────────────
        migrations.RemoveField(model_name='historicalticket', name='category'),
        migrations.RemoveField(model_name='historicalticket', name='flags'),
        migrations.RemoveField(model_name='historicalticket', name='channel'),
        migrations.RemoveField(model_name='historicalticket', name='priority'),

        # ── 4. Add FK fields to ticket ───────────────────────────────────────
        migrations.AddField(
            model_name='ticket',
            name='category',
            field=models.ForeignKey(
                blank=True, db_column='CategoryID', null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name='tickets',
                to='grievance_social_protection.ticketcategory',
            ),
        ),
        migrations.AddField(
            model_name='ticket',
            name='flags',
            field=models.ForeignKey(
                blank=True, db_column='FlagID', null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name='tickets',
                to='grievance_social_protection.ticketflag',
            ),
        ),
        migrations.AddField(
            model_name='ticket',
            name='channel',
            field=models.ForeignKey(
                blank=True, db_column='ChannelID', null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name='tickets',
                to='grievance_social_protection.ticketchannel',
            ),
        ),
        migrations.AddField(
            model_name='ticket',
            name='priority',
            field=models.ForeignKey(
                blank=True, db_column='PriorityID', null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name='tickets',
                to='grievance_social_protection.ticketpriority',
            ),
        ),

        # ── 5. Add integer FK-id fields to historicalticket ─────────────────
        migrations.AddField(
            model_name='historicalticket',
            name='category_id',
            field=models.IntegerField(blank=True, db_column='CategoryID', null=True),
        ),
        migrations.AddField(
            model_name='historicalticket',
            name='flags_id',
            field=models.IntegerField(blank=True, db_column='FlagID', null=True),
        ),
        migrations.AddField(
            model_name='historicalticket',
            name='channel_id',
            field=models.IntegerField(blank=True, db_column='ChannelID', null=True),
        ),
        migrations.AddField(
            model_name='historicalticket',
            name='priority_id',
            field=models.IntegerField(blank=True, db_column='PriorityID', null=True),
        ),
    ]
