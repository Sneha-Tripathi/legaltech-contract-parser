from django.db import models
from django.contrib.auth.models import User


class Contract(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    title = models.CharField(
        max_length=255
    )

    uploaded_file = models.FileField(
        upload_to="contracts/"
    )

    extracted_text = models.TextField(
        blank=True,
        null=True
    )

    summary = models.TextField(
        blank=True,
        null=True
    )

    keywords = models.TextField(
        blank=True,
        null=True
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class ExtractedClause(models.Model):

    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE
    )

    clause_name = models.CharField(
        max_length=255
    )

    def __str__(self):
        return self.clause_name


class RiskFlag(models.Model):

    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE
    )

    risk_type = models.CharField(
        max_length=255
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.risk_type


class AIAnalysis(models.Model):
    """
    Stores AI-generated analysis for each contract.
    Created separately from Contract to avoid modifying existing table.
    """

    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name="ai_analyses"
    )

    summary = models.TextField(
        blank=True,
        default=""
    )

    risk_analysis = models.JSONField(
        blank=True,
        default=list
    )

    missing_clauses = models.JSONField(
        blank=True,
        default=list
    )

    recommendations = models.JSONField(
        blank=True,
        default=list
    )

    confidence = models.CharField(
        max_length=20,
        blank=True,
        default=""
    )

    tags = models.JSONField(
        blank=True,
        default=list
    )

    raw_response = models.JSONField(
        blank=True,
        null=True,
        help_text="Full raw JSON response from Gemini"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "AI Analysis"
        verbose_name_plural = "AI Analyses"
        ordering = ["-created_at"]

    def __str__(self):
        return f"AI Analysis for {self.contract.title} ({self.created_at.date()})"