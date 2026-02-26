import os
import uuid
from datetime import datetime as py_datetime
from core import fields
import core
from core.utils import TimeUtils
from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from graphql import ResolveInfo

from core import (
    models as core_models,
    fields,
)
from core.models import HistoryBusinessModel, User, HistoryModel
from grievance_social_protection.apps import TicketConfig


def check_if_user_or_individual(generic_field):
    individual = apps.get_model('individual', 'Individual')
    beneficiary = apps.get_model('social_protection', 'Beneficiary')
    if not isinstance(generic_field, (User, individual, beneficiary)):
        raise ValueError('Reporter must be either a User or a Beneficiary or an Individual.')


# =============================================================================
# TABELAS DE PARAMETRIZAÇÃO (Lookup Tables)
# =============================================================================

class TicketCategory(core_models.VersionedModel):
    id = models.AutoField(db_column='TicketCategoryID', primary_key=True)
    uuid = models.CharField(db_column='TicketCategoryUUID', max_length=36, default=uuid.uuid4, unique=True)
    codigo = models.CharField(db_column='Codigo', max_length=50)
    nome = models.CharField(db_column='Nome', max_length=255)
    descricao = models.CharField(db_column='Descricao', max_length=500, null=True, blank=True)
    ativo = models.BooleanField(db_column='Ativo', default=True)

    class Meta:
        managed = True
        db_table = 'tblTicketCategory'

    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class TicketChannel(core_models.VersionedModel):
    id = models.AutoField(db_column='TicketChannelID', primary_key=True)
    uuid = models.CharField(db_column='TicketChannelUUID', max_length=36, default=uuid.uuid4, unique=True)
    codigo = models.CharField(db_column='Codigo', max_length=50)
    nome = models.CharField(db_column='Nome', max_length=255)
    descricao = models.CharField(db_column='Descricao', max_length=500, null=True, blank=True)
    ativo = models.BooleanField(db_column='Ativo', default=True)

    class Meta:
        managed = True
        db_table = 'tblTicketChannel'

    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class TicketFlag(core_models.VersionedModel):
    id = models.AutoField(db_column='TicketFlagID', primary_key=True)
    uuid = models.CharField(db_column='TicketFlagUUID', max_length=36, default=uuid.uuid4, unique=True)
    codigo = models.CharField(db_column='Codigo', max_length=50)
    nome = models.CharField(db_column='Nome', max_length=255)
    descricao = models.CharField(db_column='Descricao', max_length=500, null=True, blank=True)
    ativo = models.BooleanField(db_column='Ativo', default=True)

    class Meta:
        managed = True
        db_table = 'tblTicketFlag'

    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class TicketPriority(core_models.VersionedModel):
    id = models.AutoField(db_column='TicketPriorityID', primary_key=True)
    uuid = models.CharField(db_column='TicketPriorityUUID', max_length=36, default=uuid.uuid4, unique=True)
    codigo = models.CharField(db_column='Codigo', max_length=50)
    nome = models.CharField(db_column='Nome', max_length=255)
    ordem = models.IntegerField(db_column='Ordem', default=0)
    ativo = models.BooleanField(db_column='Ativo', default=True)

    class Meta:
        managed = True
        db_table = 'tblTicketPriority'
        ordering = ['ordem']

    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class Ticket(HistoryBusinessModel):
    class TicketStatus(models.TextChoices):
        # TMP FOR NOW
        RECEIVED = 'RECEIVED', 'Received'
        OPEN = 'OPEN', 'Open'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        RESOLVED = 'RESOLVED', 'Resolved'
        REJECTED = 'REJECTED', 'Rejected'
        CLOSED = 'CLOSED', 'Closed'

    key = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=16, unique=True, blank=True, null=True)

    reporter_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING, null=True, blank=True)
    reporter_id = models.CharField(max_length=255, null=True, blank=True)
    reporter = GenericForeignKey('reporter_type', 'reporter_id')
    reporter_info = models.JSONField(null=True, blank=True)

    attending_staff = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    date_of_incident = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=20, blank=False, null=False, choices=TicketStatus.choices, default=TicketStatus.RECEIVED
    )
    priority = models.ForeignKey(
        'TicketPriority', on_delete=models.DO_NOTHING,
        db_column='PriorityID', null=True, blank=True, related_name='tickets'
    )
    due_date = models.DateField(blank=True, null=True)

    category = models.ForeignKey(
        'TicketCategory', on_delete=models.DO_NOTHING,
        db_column='CategoryID', null=True, blank=True, related_name='tickets'
    )
    flags = models.ForeignKey(
        'TicketFlag', on_delete=models.DO_NOTHING,
        db_column='FlagID', null=True, blank=True, related_name='tickets'
    )
    channel = models.ForeignKey(
        'TicketChannel', on_delete=models.DO_NOTHING,
        db_column='ChannelID', null=True, blank=True, related_name='tickets'
    )
    resolution = models.CharField(max_length=255, blank=True, null=True)

    def clean(self):
        super().clean()
        if self.reporter:
            check_if_user_or_individual(self.reporter)

    def __str__(self):
        return f"{self.title}"


    @classmethod
    def filter_queryset(cls, queryset=None):
        if queryset is None:
            queryset = cls.objects.all()
        queryset = queryset.filter(*core.filter_validity())
        return queryset

    @classmethod
    def get_queryset(cls, queryset, user):
        queryset = cls.filter_queryset(queryset)
        if isinstance(user, ResolveInfo):
            user = user.context.user
        if settings.ROW_SECURITY and user.is_anonymous:
            return queryset.filter(id=None)
        if settings.ROW_SECURITY:
            pass
        return queryset


class TicketMutation(core_models.UUIDModel, core_models.ObjectMutation):
    ticket = models.ForeignKey(Ticket, models.DO_NOTHING,
                               related_name='mutations')
    mutation = models.ForeignKey(
        core_models.MutationLog, models.DO_NOTHING, related_name='tickets')

    class Meta:
        managed = True
        db_table = "ticket_TicketMutation"


class Comment(HistoryModel):
    ticket = models.ForeignKey(Ticket, on_delete=models.DO_NOTHING, null=False, blank=False)
    commenter_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING, null=True, blank=True)
    commenter_id = models.CharField(max_length=255, null=True, blank=True)
    commenter = GenericForeignKey('commenter_type', 'commenter_id')
    comment = models.TextField(blank=False, null=False)
    is_resolution = models.BooleanField(blank=False, null=False, default=False)

    def clean(self):
        super().clean()
        if self.commenter:
            check_if_user_or_individual(self.commenter)

        if self.is_resolution:
            existing_resolved_comments = Comment.objects.filter(ticket=self.ticket, is_resolution=True)

            if self.id:
                existing_resolved_comments = existing_resolved_comments.exclude(id=self.id)

            if existing_resolved_comments.exists():
                raise ValueError("Another comment for this ticket is already marked as resolved.")


class GeneralTicketAttachmentType(models.TextChoices):
    URL = "URL"
    FILE = "FILE"


class TicketAttachmentType(core_models.VersionedModel):
    id = models.SmallIntegerField(
        db_column='TicketAttachmentTypeId', primary_key=True)
    ticket_attachment_type = models.CharField(
        db_column='TicketAttachmentType', max_length=50)
    is_autogenerated = models.BooleanField(default=False)
    ticket_general_type = models.CharField(max_length=10, default=GeneralTicketAttachmentType.FILE,
                                          choices=GeneralTicketAttachmentType.choices)

    class Meta:
        managed = True
        db_table = 'ticket_TicketAttachment_TicketAttachmentType'


class TicketAttachment(core_models.UUIDModel, core_models.UUIDVersionedModel, ):
    ticket = models.ForeignKey(
        Ticket, models.DO_NOTHING, related_name='attachments')
    general_type = models.CharField(max_length=4, choices=GeneralTicketAttachmentType.choices,
                                    default=GeneralTicketAttachmentType.FILE)
    type = models.TextField(blank=True, null=True)
    predefined_type = models.ForeignKey(TicketAttachmentType, models.DO_NOTHING, related_name='type_dropdown', null=True,
                                        blank=True)
    title = models.TextField(blank=True, null=True)
    date = fields.DateField(blank=True, default=TimeUtils.now)
    filename = models.TextField(blank=True, null=True)
    mime = models.TextField(blank=True, null=True)
    # this is not needed at the moment, but we want to move attachment to core
    # in that case module information is needed, and we want to avoid writing additional migration
    module = models.TextField(blank=False, null=True)
    # frontend contributions may lead to externalized (nas) storage for documents
    url = models.TextField(blank=True, null=True)
    # Support of BinaryField is database-related: prefer to stick to b64-encoded
    document = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "ticket_TicketAttachment"

    def __str__(self):
        return f"{self.filename}"

    def full_file_path(self):
        if not TicketConfig.tickets_attachments_root_path or not self.filename:
            return None
        return os.path.join(TicketConfig.tickets_attachments_root_path, self.filename)


class AttachmentMutation(core_models.UUIDModel, core_models.ObjectMutation):
    ticket = models.ForeignKey(TicketAttachment, models.DO_NOTHING,
                               related_name='mutations')
    mutation = models.ForeignKey(
        core_models.MutationLog, models.DO_NOTHING, related_name='attachment')

    class Meta:
        managed = True
        db_table = "ticket_AttachmentMutation"
