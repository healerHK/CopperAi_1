import os 
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
import django.core.validators as validators
from django.conf import settings
from django.contrib.gis.db import models as gis_models

User = get_user_model()

def dataset_upload_path(instance, filename):
    project_id = instance.project.id if instance.project else "unassigned"
    return f"geospatial_datasets/project_{project_id}/{filename}"

class prospectivityProject(models.Model):
    status = models.TextChoices("project status", "Planned Active Completed Archived")
    name = models.CharField(max_length=255, null=True, blank=True)
    project_code = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True)
    project_status = models.CharField(max_length=50, choices=status.choices, default='planned')  # Fixed: Use status.choices
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    user_updated = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="updated by user")
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    location = gis_models.PointField(null=True, blank=True)
    boundary = gis_models.PolygonField(null=True, blank=True)
    target_minerals = models.CharField(max_length=255, help_text="Comma-separated list")
    mineral_type = models.CharField(max_length=255, blank=True)
    historical_production = models.FloatField(blank=True, null=True, help_text="in tonnes")

    class Meta:
        unique_together = ('name', 'project_code', 'description', 'project_status')
        ordering = ['-created_date']

    def __str__(self):
        return self.name
    
class geospatialDatasets(models.Model):
    types = models.TextChoices('dataset types', "Raster Vector Tabular metadata tiff shapefiles csv xml json")
    crs_choices = models.TextChoices("crs", "GCS PCS")
    band_types = models.TextChoices("band_info", "RED GREEN BLUE")
    project = models.ForeignKey(prospectivityProject, on_delete=models.CASCADE, verbose_name="Prospectivity Project")
    dataset_names = models.TextField(unique=True)
    dataset_types = models.CharField(max_length=50, choices=types.choices)  # Fixed: Use types.choices
    file = models.FileField(upload_to=dataset_upload_path)
    crs = models.CharField(max_length=50, choices=crs_choices.choices, verbose_name="Coordinate reference system")  # Fixed: Use crs_choices.choices
    band_info = models.CharField(max_length=20, choices=band_types.choices, verbose_name="Band")  # Fixed: Use band_types.choices

    updated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'dataset_names', 'dataset_types', 'file')
        ordering = ['updated_on']

    def __str__(self):
        return f"{self.project} ({self.dataset_types})"
    
class MLmodelRun(models.Model):
    ALG_CHOICES = (
        ('SVM', 'support vector machine'),
        ('RF', 'Random Forest'),
        ('XGBOost', 'gradient boost'),
        ('CNN', 'Convolutional Neural Network'),
    )
    run_choices = models.TextChoices("status", "Pending Running Achieved Failed")
    project = models.ForeignKey(prospectivityProject, on_delete=models.CASCADE, verbose_name="ML models")
    model_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="predictive models")
    input_data = models.ManyToManyField(geospatialDatasets, verbose_name="input data")
    algorithms_used = models.CharField(max_length=100, choices=ALG_CHOICES, default='custom')
    parameters = models.JSONField(null=True, blank=True, verbose_name="configuration parameters")
    performance_metrics = models.JSONField(null=True, blank=True, verbose_name="accuracy, F1 score, Precision, Recall")
    review_result = models.FileField(upload_to=dataset_upload_path, blank=True, null=True)
    status = models.CharField(max_length=50, choices=run_choices.choices, default='pending')  # Fixed: Use run_choices.choices
    predicted_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.model_name} ({self.status})"