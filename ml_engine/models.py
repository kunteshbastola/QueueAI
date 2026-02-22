from django.db import models
from queue_system.models import Token

class MLPrediction(models.Model):

    MODEL_CHOICES = [
        ('linear_regression', 'Linear Regression'),
        ('collaborative_filtering', 'Collaborative Filtering'),
    ]

    prediction_id = models.AutoField(primary_key=True)

    model_type = models.CharField(
        max_length=50,
        choices=MODEL_CHOICES
    )

    token = models.ForeignKey(
        'queue_system.Token',
        on_delete=models.CASCADE,
        related_name='ml_predictions',
        null=True,
        blank=True
    )

    predicted_value = models.FloatField()
    actual_value = models.FloatField(null=True, blank=True)

    features = models.JSONField(
        help_text="Input features used for prediction"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.model_type} - Token {self.token_id}"

    class Meta:
        db_table = "ml_predictions"
