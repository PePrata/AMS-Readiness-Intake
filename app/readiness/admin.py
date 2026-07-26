from django.contrib import admin
from .models import UserRole, Assessment, ReadinessQuestion, Answer, Evidence, AuditLog

admin.site.register(UserRole)
admin.site.register(Assessment)
admin.site.register(ReadinessQuestion)
admin.site.register(Answer)
admin.site.register(Evidence)
admin.site.register(AuditLog)
