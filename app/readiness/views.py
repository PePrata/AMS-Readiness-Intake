from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages

from .models import Assessment, Answer, Evidence, ReadinessQuestion, UserRole, AuditLog
from .forms import AnswerForm, EvidenceForm, RoleSelectForm
from .readiness_rules import get_missing_critical_items, can_submit, is_evidence_stale
from .audit import log_action


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_or_create_assessment():
    """Return the single working assessment, creating it if needed."""
    assessment = Assessment.objects.first()
    if assessment is None:
        creator = UserRole.objects.first()
        if creator is None:
            return None
        assessment = Assessment.objects.create(created_by=creator)
    return assessment


def _current_role(request):
    """Retrieve the UserRole stored in the session, or None."""
    role_id = request.session.get("role_id")
    if not role_id:
        return None
    try:
        return UserRole.objects.get(pk=role_id)
    except UserRole.DoesNotExist:
        return None


# ---------------------------------------------------------------------------
# Home / dashboard
# ---------------------------------------------------------------------------

def home(request):
    """
    Main hub: role selector, question list with answer/evidence status,
    last submission result, and submit button.
    """
    assessment = _get_or_create_assessment()

    # Handle role selection (POST with set_role flag)
    if request.method == "POST" and "set_role" in request.POST:
        form = RoleSelectForm(request.POST)
        if form.is_valid():
            request.session["role_id"] = form.cleaned_data["role_id"].pk
            return redirect("home")
    else:
        form = RoleSelectForm()

    current_role = _current_role(request)

    # Build per-question status
    answers_map = {}
    if assessment:
        for a in Answer.objects.filter(assessment=assessment).prefetch_related("evidence_items"):
            answers_map[a.question_id] = a

    question_data = []
    for q in ReadinessQuestion.objects.all().order_by("category", "id"):
        answer = answers_map.get(q.id)
        evidence_items = list(answer.evidence_items.all()) if answer else []
        has_fresh = any(not is_evidence_stale(e.freshness_date) for e in evidence_items)
        question_data.append(
            {
                "question": q,
                "answer": answer,
                "evidence_count": len(evidence_items),
                "has_fresh_evidence": has_fresh,
            }
        )

    missing = get_missing_critical_items(assessment) if assessment else []

    # Consume single-use result message from session
    last_result = request.session.pop("last_result", None)

    return render(
        request,
        "readiness/home.html",
        {
            "assessment": assessment,
            "current_role": current_role,
            "role_form": form,
            "question_data": question_data,
            "missing": missing,
            "last_result": last_result,
            "all_roles": UserRole.objects.all(),
        },
    )


# ---------------------------------------------------------------------------
# Answer a question (Contributor workflow — REQ-002)
# ---------------------------------------------------------------------------

def answer_question(request, question_id):
    """
    GET  — show the answer form for a specific ReadinessQuestion.
    POST — save the answer (create or update).

    Only checks role for display messaging; actual enforcement is on submit.
    """
    question = get_object_or_404(ReadinessQuestion, pk=question_id)
    assessment = _get_or_create_assessment()
    current_role = _current_role(request)

    # Fetch existing answer if any
    existing = Answer.objects.filter(assessment=assessment, question=question).first()

    if request.method == "POST":
        is_update = existing is not None
        old_response = existing.response if existing else None

        form = AnswerForm(request.POST, instance=existing, assessment=assessment)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.assessment = assessment
            answer.question = question
            answer.save()
            if current_role:
                log_action(
                    assessment=assessment,
                    actor=current_role,
                    action_type="UPDATE" if is_update else "CREATE",
                    entity_type="Answer",
                    entity_id=answer.pk,
                    field_changed="response",
                    old_value=old_response,
                    new_value=answer.response,
                    justification="Answer updated" if is_update else "Answer created",
                )
            messages.success(request, f"Answer saved: {answer.response}")
            return redirect("answer_question", question_id=question_id)
    else:
        initial = {"question": question.pk}
        form = AnswerForm(instance=existing, assessment=assessment, initial=initial)

    evidence_items = []
    if existing:
        evidence_items = list(
            existing.evidence_items.all().order_by("freshness_date")
        )
        for ev in evidence_items:
            ev.is_stale = is_evidence_stale(ev.freshness_date)

    return render(
        request,
        "readiness/answer_form.html",
        {
            "form": form,
            "question": question,
            "assessment": assessment,
            "current_role": current_role,
            "existing_answer": existing,
            "evidence_items": evidence_items,
        },
    )


# ---------------------------------------------------------------------------
# Add evidence to an answer (REQ-003)
# ---------------------------------------------------------------------------

def add_evidence(request, answer_id):
    """
    GET  — show the evidence form.
    POST — validate and save evidence metadata.

    REQ-003: source, owner, and freshness_date are all required.
    Form validation rejects the save and shows which fields are missing.
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    current_role = _current_role(request)

    if request.method == "POST":
        form = EvidenceForm(request.POST)
        if form.is_valid():
            evidence = form.save(commit=False)
            evidence.answer = answer
            evidence.full_clean()
            evidence.save()
            if current_role:
                log_action(
                    assessment=answer.assessment,
                    actor=current_role,
                    action_type="CREATE",
                    entity_type="Evidence",
                    entity_id=evidence.pk,
                    field_changed="source",
                    old_value=None,
                    new_value=evidence.source,
                    justification="Evidence created",
                )
            messages.success(request, "Evidence saved successfully.")
            return redirect("answer_question", question_id=answer.question_id)
    else:
        form = EvidenceForm()

    return render(
        request,
        "readiness/evidence_form.html",
        {
            "form": form,
            "answer": answer,
            "current_role": current_role,
        },
    )


# ---------------------------------------------------------------------------
# Submit assessment (REQ-005 / REQ-008)
# ---------------------------------------------------------------------------

def submit_assessment(request):
    """
    POST-only: attempt to submit the assessment.

    Rules enforced by readiness_rules.can_submit():
    - Role must be "Transition Lead".
    - All critical questions must have at least one non-stale evidence item.

    Any other role → authorization error (not silently ignored).
    """
    if request.method != "POST":
        return redirect("home")

    current_role = _current_role(request)
    if current_role is None:
        request.session["last_result"] = {
            "success": False,
            "error": "No role selected. Please choose a role before submitting.",
        }
        return redirect("home")

    assessment = _get_or_create_assessment()
    if assessment is None:
        request.session["last_result"] = {
            "success": False,
            "error": "No assessment found.",
        }
        return redirect("home")

    if assessment.status == "Submitted":
        request.session["last_result"] = {
            "success": False,
            "error": "This assessment has already been submitted.",
        }
        return redirect("home")

    allowed, error = can_submit(assessment, current_role)
    if not allowed:
        request.session["last_result"] = {"success": False, "error": error}
    else:
        old_status = assessment.status
        assessment.status = "Submitted"
        assessment.submitted_by = current_role
        assessment.submitted_at = timezone.now()
        assessment.save()
        log_action(
            assessment=assessment,
            actor=current_role,
            action_type="UPDATE",
            entity_type="Assessment",
            entity_id=assessment.pk,
            field_changed="status",
            old_value=old_status,
            new_value="Submitted",
            justification="Assessment submitted",
        )
        request.session["last_result"] = {
            "success": True,
            "message": (
                f"Assessment #{assessment.pk} submitted successfully by "
                f"{current_role.name} ({current_role.role})."
            ),
        }

    return redirect("home")


# ---------------------------------------------------------------------------
# Summary view (REQ-004, REQ-006)
# ---------------------------------------------------------------------------

def summary(request):
    """
    Dedicated summary page showing:
    - Current assessment status (Draft / Submitted)
    - Critical questions still missing valid evidence, with the specific reason
    - Last submission attempt result
    """
    assessment = _get_or_create_assessment()
    current_role = _current_role(request)

    missing = get_missing_critical_items(assessment) if assessment else []
    last_result = request.session.pop("last_result", None)

    answered_count = Answer.objects.filter(assessment=assessment).count() if assessment else 0
    total_critical = ReadinessQuestion.objects.filter(is_critical=True).count()
    audit_entries = (
        assessment.audit_entries.all().order_by("timestamp") if assessment else AuditLog.objects.none()
    )

    return render(
        request,
        "readiness/summary.html",
        {
            "assessment": assessment,
            "current_role": current_role,
            "missing": missing,
            "last_result": last_result,
            "answered_count": answered_count,
            "total_critical": total_critical,
            "audit_entries": audit_entries,
        },
    )
