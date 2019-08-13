"""
Practice groups refer to practices that are "the same" but
with different levels of specificity. For example, a practice
suggesting to add a "culture étouffate" and another one suggesting
to add "Chanvre" (which is a culture étouffante) are the same, so
we should avoid suggesting both at the same time.
"""
import uuid
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

class PracticeGroup(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_id = models.CharField(max_length=100)
    modification_date = models.DateTimeField()
    creation_date = models.DateTimeField(default=timezone.now)

    airtable_json = JSONField(null=True, blank=True)

    name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
