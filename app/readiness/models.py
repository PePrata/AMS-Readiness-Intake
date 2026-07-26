from django.db import models
from django.core.exceptions import ValidationError

from .audit import validate_entity_reference


class UserRole(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(
        max_length=20,
        choices=[
            ("Transition Lead", "Transition Lead"),
            ("AMS Manager", "AMS Manager"),
            ("Contributor", "Contributor"),
            ("Security Officer", "Security Officer"),
        ],
    )

    def __str__(self):
        return f"{self.name} ({self.role})"


class Assessment(models.Model):
    status = models.CharField(
        max_length=10,
        choices=[("Draft", "Draft"), ("Submitted", "Submitted")],
        default="Draft",
    )
    created_by = models.ForeignKey(
        UserRole,
        on_delete=models.PROTECT,
        related_name="created_assessments",
    )
    created_at = models.DateField(auto_now_add=True)
    submitted_by = models.ForeignKey(
        UserRole,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="submitted_assessments",
    )
    submitted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Assessment #{self.pk} [{self.status}]"


class ReadinessQuestion(models.Model):
    text = models.CharField(max_length=255)
    category = models.CharField(max_length=50)  # monitoring / DR / access / integrations / SLA
    is_critical = models.BooleanField(default=True)

    def __str__(self):
        return f"[{self.category}] {self.text}"


class Answer(models.Model):
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    question = models.ForeignKey(
        ReadinessQuestion,
        on_delete=models.PROTECT,
    )
    response = models.CharField(
        max_length=10,
        choices=[("Yes", "Yes"), ("No", "No"), ("Partial", "Partial")],
    )
    note = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("assessment", "question")

    def __str__(self):
        return f"Answer to Q{self.question_id}: {self.response}"


class Evidence(models.Model):
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name="evidence_items",
    )
    source = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    freshness_date = models.DateField()
    reference = models.CharField(max_length=255)  # link/URL or short description

    def clean(self):
        """REQ-003: Evidence cannot be saved without source, owner AND freshness_date."""
        errors = {}
        if not self.source or not self.source.strip():
            errors["source"] = "Source is required."
        if not self.owner or not self.owner.strip():
            errors["owner"] = "Owner is required."
        if self.freshness_date is None:
            errors["freshness_date"] = "Freshness date is required."
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Evidence for Answer #{self.answer_id}: {self.source}"


class AuditLog(models.Model):
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="audit_entries",
    )
    actor = models.ForeignKey(UserRole, on_delete=models.PROTECT)
    role = models.CharField(max_length=20)
    action_type = models.CharField(
        max_length=10,
        choices=[("CREATE", "Create"), ("UPDATE", "Update"), ("DELETE", "Delete")],
    )
    entity_type = models.CharField(
        max_length=20,
        choices=[
            ("Assessment", "Assessment"),
            ("Answer", "Answer"),
            ("Evidence", "Evidence"),
        ],
    )
    entity_id = models.PositiveIntegerField()
    field_changed = models.CharField(max_length=100, blank=True, null=True)
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    justification = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def clean(self):
        super().clean()
        validate_entity_reference(self)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.action_type} {self.entity_type}#{self.entity_id}"
