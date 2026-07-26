from django import forms
from django.core.exceptions import ValidationError

from .models import Answer, Evidence, ReadinessQuestion, UserRole


class RoleSelectForm(forms.Form):
    """Simulates choosing an acting role — no Django auth required (REQ-008)."""

    role_id = forms.ModelChoiceField(
        queryset=UserRole.objects.all(),
        label="Acting as",
        empty_label="— select a role —",
        widget=forms.Select(attrs={"class": "role-select"}),
    )


class AnswerForm(forms.ModelForm):
    """
    REQ-002: Contributor submits a readiness question response (Yes / No / Partial).
    """

    class Meta:
        model = Answer
        fields = ["question", "response", "note"]
        widgets = {
            "question": forms.HiddenInput(),
            "note": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, assessment=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.assessment = assessment

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.assessment:
            instance.assessment = self.assessment
        if commit:
            instance.save()
        return instance


class EvidenceForm(forms.ModelForm):
    """
    REQ-003: Evidence metadata — source, owner, freshness_date are all required.
    Validation is enforced both via the model's clean() and here in the form.
    """

    class Meta:
        model = Evidence
        fields = ["source", "owner", "freshness_date", "reference"]
        widgets = {
            "freshness_date": forms.DateInput(attrs={"type": "date"}),
            "reference": forms.TextInput(attrs={"placeholder": "URL or short description"}),
        }

    def clean_source(self):
        value = self.cleaned_data.get("source", "").strip()
        if not value:
            raise ValidationError("Source is required (REQ-003).")
        return value

    def clean_owner(self):
        value = self.cleaned_data.get("owner", "").strip()
        if not value:
            raise ValidationError("Owner is required (REQ-003).")
        return value

    def clean_freshness_date(self):
        value = self.cleaned_data.get("freshness_date")
        if value is None:
            raise ValidationError("Freshness date is required (REQ-003).")
        return value
