from django.apps import apps
from django.core.exceptions import ValidationError


def validate_entity_reference(audit_log):
    """Ensure the polymorphic entity reference exists for CREATE/UPDATE actions."""
    if audit_log.action_type == "DELETE":
        return

    try:
        model_class = apps.get_model("readiness", audit_log.entity_type)
    except LookupError as exc:
        raise ValidationError({"entity_type": "Unsupported entity type."}) from exc

    if not model_class.objects.filter(pk=audit_log.entity_id).exists():
        raise ValidationError(
            {
                "entity_id": (
                    f"No {audit_log.entity_type.lower()} exists with id {audit_log.entity_id}."
                )
            }
        )


def log_action(
    assessment,
    actor,
    action_type,
    entity_type,
    entity_id,
    field_changed=None,
    old_value=None,
    new_value=None,
    justification=None,
):
    """Create a read-only audit log entry for the given entity change."""
    from .models import AuditLog

    if actor is None:
        raise ValueError("An actor is required to create an audit log entry.")

    entry = AuditLog(
        assessment=assessment,
        actor=actor,
        role=actor.role,
        action_type=action_type,
        entity_type=entity_type,
        entity_id=entity_id,
        field_changed=field_changed,
        old_value=old_value,
        new_value=new_value,
        justification=justification,
    )
    entry.full_clean()
    entry.save()
    return entry
