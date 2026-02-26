import base64
import pathlib
from urllib.parse import urlparse
import uuid
from core.utils import filter_validity
from django.conf import settings
import graphene
from graphql_relay import from_global_id

from core.gql.gql_mutations.base_mutation import BaseHistoryModelCreateMutationMixin, BaseMutation, \
    BaseHistoryModelUpdateMutationMixin, BaseHistoryModelDeleteMutationMixin
from core.schema import OpenIMISMutation
from .models import (
    GeneralTicketAttachmentType, Ticket, TicketAttachment, TicketAttachmentType, TicketMutation, Comment,
    TicketCategory, TicketChannel, TicketFlag, TicketPriority,
)

from django.core.exceptions import ValidationError, PermissionDenied
from .apps import TicketConfig
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .services import TicketService, CommentService
from .validations import user_associated_with_ticket


# =============================================================================
# Lookup table mutations — TicketCategory
# =============================================================================

class TicketCategoryInputType(OpenIMISMutation.Input):
    codigo = graphene.String(required=True)
    nome = graphene.String(required=True)
    descricao = graphene.String(required=False)
    ativo = graphene.Boolean(required=False)


class CreateTicketCategoryMutation(OpenIMISMutation):
    _mutation_module = "grievance_social_protection"
    _mutation_class = "CreateTicketCategoryMutation"

    class Input(TicketCategoryInputType):
        pass

    @classmethod
    def async_mutate(cls, user, **data):
        try:
            if not user.has_perms(TicketConfig.gql_mutation_create_tickets_perms):
                raise PermissionDenied(_("unauthorized"))
            data.pop('client_mutation_id', None)
            data.pop('client_mutation_label', None)
            obj = TicketCategory(**data)
            obj.audit_user_id = user.id_for_audit
            obj.save()
            return None
        except Exception as exc:
            return [{'message': str(exc), 'detail': str(exc)}]


class UpdateTicketCategoryMutation(OpenIMISMutation):
    _mutation_module = "grievance_social_protection"
    _mutation_class = "UpdateTicketCategoryMutation"

    class Input(TicketCategoryInputType):
        id = graphene.String(required=True)

    @classmethod
    def async_mutate(cls, user, **data):
        try:
            if not user.has_perms(TicketConfig.gql_mutation_update_tickets_perms):
                raise PermissionDenied(_("unauthorized"))
            data.pop('client_mutation_id', None)
            data.pop('client_mutation_label', None)
            _, pk = from_global_id(data.pop('id'))
            obj = TicketCategory.objects.get(pk=pk, validity_to__isnull=True)
            for key, value in data.items():
                setattr(obj, key, value)
            obj.audit_user_id = user.id_for_audit
            obj.save()
            return None
        except Exception as exc:
            return [{'message': str(exc), 'detail': str(exc)}]


class DeleteTicketCategoryMutation(OpenIMISMutation):
    _mutation_module = "grievance_social_protection"
    _mutation_class = "DeleteTicketCategoryMutation"

    class Input(OpenIMISMutation.Input):
        id = graphene.String(required=True)

    @classmethod
    def async_mutate(cls, user, **data):
        try:
            if not user.has_perms(TicketConfig.gql_mutation_delete_tickets_perms):
                raise PermissionDenied(_("unauthorized"))
            _, pk = from_global_id(data['id'])
            obj = TicketCategory.objects.get(pk=pk, validity_to__isnull=True)
            obj.validity_to = timezone.now()
            obj.save()
            return None
        except Exception as exc:
            return [{'message': str(exc), 'detail': str(exc)}]


# =============================================================================
# Lookup table mutations — TicketChannel
# =============================================================================

class TicketChannelInputType(OpenIMISMutation.Input):
    codigo = graphene.String(required=True)
    nome = graphene.String(required=True)
    descricao = graphene.String(required=False)
    ativo = graphene.Boolean(required=False)


class CreateTicketChannelMutation(OpenIMISMutation):
    _mutation_module = "grievance_social_protection"
    _mutation_class = "CreateTicketChannelMutation"

    class Input(TicketChannelInputType):
        pass

    @classmethod
    def async_mutate(cls, user, **data):
        try:
            if not user.has_perms(TicketConfig.gql_mutation_create_tickets_perms):
                raise PermissionDenied(_("unauthorized"))
            data.pop('client_mutation_id', None)
            data.pop('client_mutation_label', None)
            obj = TicketChannel(**data)
            obj.audit_user_id = user.id_for_audit
            obj.save()
            return None
        except Exception as exc:
            return [{'message': str(exc), 'detail': str(exc)}]


class UpdateTicketChannelMutation(OpenIMISMutation):
    _mutation_module = "grievance_social_protection"
    _mutation_class = "UpdateTicketChannelMutation"

    class Input(TicketChannelInputType):
        id = graphene.String(required=True)

    @classmethod
    def async_mutate(cls, user, **data):
        try:
            if not user.has_perms(TicketConfig.gql_mutation_update_tickets_perms):
                raise PermissionDenied(_("unauthorized"))
            data.pop('client_mutation_id', None)
            data.pop('client_mutation_label', None)
            _, pk = from_global_id(data.pop('id'))
            obj = TicketChannel.objects.get(pk=pk, validity_to__isnull=True)
            for key, value in data.items():
                setattr(obj, key, value)
            obj.audit_user_id = user.id_for_audit
            obj.save()
            return None
        except Exception as exc:
            return [{'message': str(exc), 'detail': str(exc)}]


class DeleteTicketChannelMutation(OpenIMISMutation):
    _mutation_module = "grievance_social_protection"
    _mutation_class = "DeleteTicketChannelMutation"

    class Input(OpenIMISMutation.Input):
        id = graphene.String(required=True)

    @classmethod
    def async_mutate(cls, user, **data):
        try:
            if not user.has_perms(TicketConfig.gql_mutation_delete_tickets_perms):
                raise PermissionDenied(_("unauthorized"))
            _, pk = from_global_id(data['id'])
            obj = TicketChannel.objects.get(pk=pk, validity_to__isnull=True)
            obj.validity_to = timezone.now()
            obj.save()
            return None
        except Exception as exc:
            return [{'message': str(exc), 'detail': str(exc)}]


# =============================================================================
# Lookup table mutations — TicketFlag
# =============================================================================

class TicketFlagInputType(OpenIMISMutation.Input):
    codigo = graphene.String(required=True)
    nome = graphene.String(required=True)
    descricao = graphene.String(required=False)
    ativo = graphene.Boolean(required=False)


class CreateTicketFlagMutation(OpenIMISMutation):
    _mutation_module = "grievance_social_protection"
    _mutation_class = "CreateTicketFlagMutation"

    class Input(TicketFlagInputType):
        pass

    @classmethod
    def async_mutate(cls, user, **data):
        try:
            if not user.has_perms(TicketConfig.gql_mutation_create_tickets_perms):
                raise PermissionDenied(_("unauthorized"))
            data.pop('client_mutation_id', None)
            data.pop('client_mutation_label', None)
            obj = TicketFlag(**data)
            obj.audit_user_id = user.id_for_audit
            obj.save()
            return None
        except Exception as exc:
            return [{'message': str(exc), 'detail': str(exc)}]


class UpdateTicketFlagMutation(OpenIMISMutation):
    _mutation_module = "grievance_social_protection"
    _mutation_class = "UpdateTicketFlagMutation"

    class Input(TicketFlagInputType):
        id = graphene.String(required=True)

    @classmethod
    def async_mutate(cls, user, **data):
        try:
            if not user.has_perms(TicketConfig.gql_mutation_update_tickets_perms):
                raise PermissionDenied(_("unauthorized"))
            data.pop('client_mutation_id', None)
            data.pop('client_mutation_label', None)
            _, pk = from_global_id(data.pop('id'))
            obj = TicketFlag.objects.get(pk=pk, validity_to__isnull=True)
            for key, value in data.items():
                setattr(obj, key, value)
            obj.audit_user_id = user.id_for_audit
            obj.save()
            return None
        except Exception as exc:
            return [{'message': str(exc), 'detail': str(exc)}]


class DeleteTicketFlagMutation(OpenIMISMutation):
    _mutation_module = "grievance_social_protection"
    _mutation_class = "DeleteTicketFlagMutation"

    class Input(OpenIMISMutation.Input):
        id = graphene.String(required=True)

    @classmethod
    def async_mutate(cls, user, **data):
        try:
            if not user.has_perms(TicketConfig.gql_mutation_delete_tickets_perms):
                raise PermissionDenied(_("unauthorized"))
            _, pk = from_global_id(data['id'])
            obj = TicketFlag.objects.get(pk=pk, validity_to__isnull=True)
            obj.validity_to = timezone.now()
            obj.save()
            return None
        except Exception as exc:
            return [{'message': str(exc), 'detail': str(exc)}]


# =============================================================================
# Lookup table mutations — TicketPriority
# =============================================================================

class TicketPriorityInputType(OpenIMISMutation.Input):
    codigo = graphene.String(required=True)
    nome = graphene.String(required=True)
    ordem = graphene.Int(required=False)
    ativo = graphene.Boolean(required=False)


class CreateTicketPriorityMutation(OpenIMISMutation):
    _mutation_module = "grievance_social_protection"
    _mutation_class = "CreateTicketPriorityMutation"

    class Input(TicketPriorityInputType):
        pass

    @classmethod
    def async_mutate(cls, user, **data):
        try:
            if not user.has_perms(TicketConfig.gql_mutation_create_tickets_perms):
                raise PermissionDenied(_("unauthorized"))
            data.pop('client_mutation_id', None)
            data.pop('client_mutation_label', None)
            obj = TicketPriority(**data)
            obj.audit_user_id = user.id_for_audit
            obj.save()
            return None
        except Exception as exc:
            return [{'message': str(exc), 'detail': str(exc)}]


class UpdateTicketPriorityMutation(OpenIMISMutation):
    _mutation_module = "grievance_social_protection"
    _mutation_class = "UpdateTicketPriorityMutation"

    class Input(TicketPriorityInputType):
        id = graphene.String(required=True)

    @classmethod
    def async_mutate(cls, user, **data):
        try:
            if not user.has_perms(TicketConfig.gql_mutation_update_tickets_perms):
                raise PermissionDenied(_("unauthorized"))
            data.pop('client_mutation_id', None)
            data.pop('client_mutation_label', None)
            _, pk = from_global_id(data.pop('id'))
            obj = TicketPriority.objects.get(pk=pk, validity_to__isnull=True)
            for key, value in data.items():
                setattr(obj, key, value)
            obj.audit_user_id = user.id_for_audit
            obj.save()
            return None
        except Exception as exc:
            return [{'message': str(exc), 'detail': str(exc)}]


class DeleteTicketPriorityMutation(OpenIMISMutation):
    _mutation_module = "grievance_social_protection"
    _mutation_class = "DeleteTicketPriorityMutation"

    class Input(OpenIMISMutation.Input):
        id = graphene.String(required=True)

    @classmethod
    def async_mutate(cls, user, **data):
        try:
            if not user.has_perms(TicketConfig.gql_mutation_delete_tickets_perms):
                raise PermissionDenied(_("unauthorized"))
            _, pk = from_global_id(data['id'])
            obj = TicketPriority.objects.get(pk=pk, validity_to__isnull=True)
            obj.validity_to = timezone.now()
            obj.save()
            return None
        except Exception as exc:
            return [{'message': str(exc), 'detail': str(exc)}]


class BaseAttachment:
    id = graphene.String(required=False, read_only=True)
    type = graphene.String(required=False)
    title = graphene.String(required=False)
    date = graphene.Date(required=False)
    filename = graphene.String(required=False)
    mime = graphene.String(required=False)
    general_type = graphene.String(required=False)
    predefined_type = graphene.String(required=False)
    url = graphene.String(required=False)


class BaseAttachmentInputType(BaseAttachment, OpenIMISMutation.Input):
    """
    Ticket attachment (without the document), used on its own
    """
    ticket_uuid = graphene.String(required=False)


class Attachment(BaseAttachment):
    document = graphene.String(required=False)


class TicketAttachmentInputType(Attachment, graphene.InputObjectType):
    """
    Ticket attachment, used nested in ticket object
    """
    pass


class AttachmentInputType(Attachment, OpenIMISMutation.Input):
    """
    Ticket attachment, used on its own
    """
    ticket_uuid = graphene.String(required=False)


class CreateTicketInputType(OpenIMISMutation.Input):
    class TicketStatusEnum(graphene.Enum):
        RECEIVED = Ticket.TicketStatus.RECEIVED
        OPEN = Ticket.TicketStatus.OPEN
        IN_PROGRESS = Ticket.TicketStatus.IN_PROGRESS
        RESOLVED = Ticket.TicketStatus.RESOLVED
        REJECTED = Ticket.TicketStatus.REJECTED
        CLOSED = Ticket.TicketStatus.CLOSED

    key = graphene.String(required=False)
    title = graphene.String(required=False)
    description = graphene.String(required=False)
    reporter_type = graphene.String(required=False, max_lenght=255)
    reporter_id = graphene.String(required=False, max_lenght=255)
    reporter_info = graphene.types.json.JSONString(required=False)
    attending_staff_id = graphene.UUID(required=False)
    date_of_incident = graphene.Date(required=False)
    status = graphene.Field(TicketStatusEnum, required=False)
    priority_id = graphene.String(required=False, description="Relay ID da TicketPriority")
    due_date = graphene.Date(required=False)
    category_id = graphene.String(required=False, description="Relay ID da TicketCategory")
    flags_id = graphene.String(required=False, description="Relay ID do TicketFlag")
    channel_id = graphene.String(required=False, description="Relay ID do TicketChannel")
    resolution = graphene.String(required=False)

    attachments = graphene.List(
        TicketAttachmentInputType,
        required=False,
        description="List of attachments to be added to the ticket",
    )


class UpdateTicketInputType(CreateTicketInputType):
    id = graphene.UUID(required=True)


class ResolveGrievanceByCommentInputType(OpenIMISMutation.Input):
    id = graphene.UUID(required=True)


class CreateCommentInputType(OpenIMISMutation.Input):
    ticket_id = graphene.UUID(required=True)
    commenter_type = graphene.String(required=False, max_lenght=255)
    commenter_id = graphene.String(required=False, max_lenght=255)
    comment = graphene.String(required=True)


def create_file(date, ticket_id, document):
    date_iso = date.isoformat()
    root = TicketConfig.tickets_attachments_root_path
    file_dir = '%s/%s/%s/%s' % (
        date_iso[0:4],
        date_iso[5:7],
        date_iso[8:10],
        ticket_id
    )

    file_path = '%s/%s' % (file_dir, uuid.uuid4())
    pathlib.Path('%s/%s' % (root, file_dir)).mkdir(parents=True, exist_ok=True)
    f = open('%s/%s' % (root, file_path), "xb")
    f.write(base64.b64decode(document))
    f.close()
    return file_path


def create_attachment(ticket_id, data):
    data["ticket_id"] = ticket_id
    from core import datetime
    now = datetime.datetime.now()
    general_type = data['general_type']
    data['module'] = 'grievance_social_protection'
    if general_type == GeneralTicketAttachmentType.URL:
        parsed_url = urlparse(data['url'])
        if (TicketConfig.allowed_domains_attachments and
                not any(domain in parsed_url.path for domain in TicketConfig.allowed_domains_attachments)):
            raise ValidationError(
                _("mutation.attachment_url_domain_not_allowed"))
        data['document'] = data['url']
        data['predefined_type'] = TicketAttachmentType.objects.get(validity_to__isnull=True, ticket_general_type=general_type,
                                                                  ticket_attachment_type=data['predefined_type'])
    elif general_type == GeneralTicketAttachmentType.FILE:
        if TicketConfig.ticket_attachments_root_path:
            # don't use data date as it may be updated by user afterwards!
            data['url'] = create_file(now, ticket_id, data.pop('document'))
        data['predefined_type'] = TicketAttachmentType.objects.get(validity_to__isnull=True, ticket_general_type=general_type,
                                                                  ticket_attachment_type=data['predefined_type'])
    else:
        raise ValidationError(_("mutation.attachment_general_type_incorrect"))
    data['validity_from'] = now
    TicketAttachment.objects.create(**data)


def create_attachments(ticket_id, attachments):
    for attachment in attachments:
        create_attachment(ticket_id, attachment)


def _decode_ticket_fk_ids(data):
    """Decode Relay-encoded IDs for Ticket FK fields into integer PKs."""
    for field in ('category_id', 'flags_id', 'channel_id', 'priority_id'):
        if data.get(field):
            try:
                _, pk = from_global_id(data[field])
                data[field] = int(pk)
            except Exception:
                pass


class CreateTicketMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_class = "CreateTicketMutation"
    _mutation_module = "grievance_social_protection"
    _model = Ticket

    @classmethod
    def _validate_mutation(cls, user, **data):
        super()._validate_mutation(user, **data)
        if not user.has_perms(TicketConfig.gql_mutation_create_tickets_perms):
            raise PermissionDenied(_("unauthorized"))

    @classmethod
    def _mutate(cls, user, **data):
        client_mutation_id = data.pop('client_mutation_id')
        if "client_mutation_label" in data:
            data.pop('client_mutation_label')

        _decode_ticket_fk_ids(data)

        service = TicketService(user)
        response = service.create(data)
        if client_mutation_id:
            ticket_id = response['data']['id']
            attachments = data.pop(
                'attachments') if 'attachments' in data else None
            ticket = Ticket.objects.get(id=ticket_id)
            if attachments:
                create_attachments(ticket.id, attachments)
            TicketMutation.object_mutated(user, client_mutation_id=client_mutation_id, ticket=ticket)

        if not response['success']:
            return response
        return None

    class Input(CreateTicketInputType):
        pass


class UpdateTicketMutation(BaseHistoryModelUpdateMutationMixin, BaseMutation):
    _mutation_class = "UpdateTicketMutation"
    _mutation_module = "grievance_social_protection"
    _model = Ticket

    @classmethod
    def _validate_mutation(cls, user, **data):
        super()._validate_mutation(user, **data)
        if not user.has_perms(TicketConfig.gql_mutation_update_tickets_perms):
            raise PermissionDenied(_("unauthorized"))

    @classmethod
    def _mutate(cls, user, **data):
        client_mutation_id = data.pop('client_mutation_id')
        if "client_mutation_label" in data:
            data.pop('client_mutation_label')

        _decode_ticket_fk_ids(data)

        service = TicketService(user)
        response = service.update(data)
        if client_mutation_id:
            ticket_id = response['data']['id']
            ticket = Ticket.objects.get(id=ticket_id)
            TicketMutation.object_mutated(user, client_mutation_id=client_mutation_id, ticket=ticket)
        if not response['success']:
            return response
        return None

    class Input(UpdateTicketInputType):
        pass


class DeleteTicketMutation(BaseHistoryModelDeleteMutationMixin, BaseMutation):
    _mutation_class = "DeleteTicketMutation"
    _mutation_module = "grievance_social_protection"
    _model = Ticket

    @classmethod
    def _validate_mutation(cls, user, **data):
        super()._validate_mutation(user, **data)
        if not user.has_perms(
                TicketConfig.gql_mutation_delete_tickets_perms):
            raise ValidationError("mutation.authentication_required")

    class Input(OpenIMISMutation.Input):
        ids = graphene.List(graphene.UUID)


class CreateTicketAttachmentMutation(BaseHistoryModelDeleteMutationMixin, BaseMutation):
    _mutation_class = "CreateTicketAttachmentMutation"
    _mutation_module = "grievance_social_protection"
    _model = TicketAttachment

    class Input(AttachmentInputType):
        pass
    
    @classmethod
    def _validate_mutation(cls, user, **data):
        super()._validate_mutation(user, **data)
        if not user.has_perms(
                TicketConfig.gql_mutation_create_tickets_perms):
            raise ValidationError("mutation.authentication_required")

    @classmethod
    def async_mutate(cls, user, **data):
        ticket = None
        try:
            if user.is_anonymous or not user.has_perms(TicketConfig.gql_mutation_update_tickets_perms):
                raise PermissionDenied(_("unauthorized"))
            if "client_mutation_id" in data:
                data.pop('client_mutation_id')
            if "client_mutation_label" in data:
                data.pop('client_mutation_label')
            ticket_uuid = data.pop("ticket_uuid")
            queryset = Ticket.objects.filter(*filter_validity())
            ticket = queryset.filter(uuid=ticket_uuid).first()
            if not ticket:
                raise PermissionDenied(_("unauthorized"))
            create_attachment(ticket.id, data)
            return None
        except Exception as exc:
            return [{
                'message': _("ticket.mutation.failed_to_attach_document") % {'code': ticket.code if ticket else None},
                'detail': str(exc)}]


class UpdateTicketAttachmentMutation(BaseHistoryModelDeleteMutationMixin, BaseMutation):
    _mutation_class = "UpdateTicketAttachmentMutation"
    _mutation_module = "grievance_social_protection"
    _model = TicketAttachment

    class Input(BaseAttachmentInputType):
        pass
    
    @classmethod
    def _validate_mutation(cls, user, **data):
        super()._validate_mutation(user, **data)
        if not user.has_perms(
                TicketConfig.gql_mutation_update_tickets_perms):
            raise ValidationError("mutation.authentication_required")

    @classmethod
    def async_mutate(cls, user, **data):
        try:
            if not user.has_perms(TicketConfig.gql_mutation_update_tickets_perms):
                raise PermissionDenied(_("unauthorized"))
            queryset = TicketAttachment.objects.filter(*filter_validity())
 
            attachment = queryset \
                .filter(id=data['id']) \
                .first()
            if not attachment:
                raise PermissionDenied(_("unauthorized"))
            general_type = data['general_type']
            data['module'] = 'grievance_social_protection'
            from core import datetime
            now = datetime.datetime.now()
            if general_type == GeneralTicketAttachmentType.URL:
                parsed_url = urlparse(data['url'])
                if (TicketConfig.allowed_domains_attachments and
                        not any(domain in parsed_url.path for domain in TicketConfig.allowed_domains_attachments)):
                    raise ValidationError(
                        _("mutation.attachment_url_domain_not_allowed"))
                data['document'] = data['url']
                data['predefined_type'] = TicketAttachmentType.objects.get(validity_to__isnull=True,
                                                                          ticket_general_type=general_type,
                                                                          ticket_attachment_type=data['predefined_type'])
            elif general_type == GeneralTicketAttachmentType.FILE:
                if TicketConfig.ticket_attachments_root_path:
                    # don't use data date as it may be updated by user afterwards!
                    data['url'] = create_file(
                        now, data['ticket_id'], data.pop('document'))
                data['predefined_type'] = TicketAttachmentType.objects.get(validity_to__isnull=True,
                                                                          ticket_general_type=general_type,
                                                                          ticket_attachment_type=data['predefined_type'])
            attachment.save_history()
            data['audit_user_id'] = user.id_for_audit
            [setattr(attachment, key, data[key]) for key in data]
            attachment.save()
            return None
        except Exception as exc:
            return [{
                'message': _("ticket.mutation.failed_to_update_ticket_attachment") % {
                    'code': attachment.ticket.code,
                    'filename': attachment.filename
                },
                'detail': str(exc)}]


class DeleteTicketAttachmentMutation(OpenIMISMutation):
    _mutation_class = "DeleteTicketAttachmentMutation"
    _mutation_module = "grievance_social_protection"

    class Input(OpenIMISMutation.Input):
        id = graphene.String()

    @classmethod
    def async_mutate(cls, user, **data):
        try:
            if not user.has_perms(TicketConfig.gql_mutation_update_tickets_perms):
                raise PermissionDenied(_("unauthorized"))
            queryset = TicketAttachment.objects.filter(*filter_validity())
            attachment = queryset \
                .filter(id=data['id']) \
                .first()
            if not attachment:
                raise PermissionDenied(_("unauthorized"))
            attachment.delete_history()
            return None
        except Exception as exc:
            return [{
                'message': _("ticket.mutation.failed_to_delete_ticket_attachment") % {
                    'code': attachment.ticket.code,
                    'filename': attachment.filename
                },
                'detail': str(exc)}]


class CreateCommentMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_class = "CreateCommentMutation"
    _mutation_module = "grievance_social_protection"
    _model = Comment

    @classmethod
    def _validate_mutation(cls, user, **data):
        super()._validate_mutation(user, **data)
        if user.has_perms(TicketConfig.gql_mutation_delete_tickets_perms):
            return
        if user_associated_with_ticket(user):
            return
        raise ValidationError("mutation.authentication_required")

    @classmethod
    def _mutate(cls, user, **data):
        if "client_mutation_id" in data:
            data.pop('client_mutation_id')
        if "client_mutation_label" in data:
            data.pop('client_mutation_label')

        if "commenter_type" in data:
            data['commenter_type'] = data.get('commenter_type', '').lower()
        service = CommentService(user)
        response = service.create(data)

        if not response['success']:
            return response
        return None

    class Input(CreateCommentInputType):
        pass


class ResolveGrievanceByCommentMutation(BaseHistoryModelUpdateMutationMixin, BaseMutation):
    _mutation_class = "ResolveGrievanceByCommentMutation"
    _mutation_module = "grievance_social_protection"
    _model = Comment

    @classmethod
    def _validate_mutation(cls, user, **data):
        super()._validate_mutation(user, **data)
        if not user.has_perms(TicketConfig.gql_mutation_resolve_grievance_perms):
            raise ValidationError("mutation.authentication_required")

    @classmethod
    def _mutate(cls, user, **data):
        client_mutation_id = data.pop('client_mutation_id')
        if "client_mutation_label" in data:
            data.pop('client_mutation_label')

        service = CommentService(user)
        response = service.resolve_grievance_by_comment(data)
        if client_mutation_id:
            comment_id = data.get('id')
            ticket = Comment.objects.get(id=comment_id).ticket
            TicketMutation.object_mutated(user, client_mutation_id=client_mutation_id, ticket=ticket)

        if not response['success']:
            return response
        return None

    class Input(ResolveGrievanceByCommentInputType):
        pass


class ReopenTicketMutation(BaseHistoryModelUpdateMutationMixin, BaseMutation):
    _mutation_class = "ReopenTicketMutation"
    _mutation_module = "grievance_social_protection"
    _model = Ticket

    @classmethod
    def _validate_mutation(cls, user, **data):
        super()._validate_mutation(user, **data)
        if not user.has_perms(TicketConfig.gql_mutation_update_tickets_perms):
            raise ValidationError("mutation.authentication_required")

    @classmethod
    def _mutate(cls, user, **data):
        client_mutation_id = data.pop('client_mutation_id')
        if "client_mutation_label" in data:
            data.pop('client_mutation_label')

        service = TicketService(user)
        response = service.reopen_ticket(data)
        if client_mutation_id:
            ticket_id = data.get('id')
            ticket = Ticket.objects.get(id=ticket_id)
            TicketMutation.object_mutated(user, client_mutation_id=client_mutation_id, Ticket=ticket)

        if not response['success']:
            return response
        return None

    class Input(ResolveGrievanceByCommentInputType):
        pass
