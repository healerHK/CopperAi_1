
from django import forms
from .models import prospectivityProject, geospatialDatasets

class ProspectivityProjectForm(forms.ModelForm):
    class Meta:
        model = prospectivityProject
        fields = ['name', 'project_code', 'description', 'project_status', 'country', 'region', 'target_minerals', 'mineral_type']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class GeospatialDatasetForm(forms.ModelForm):
    class Meta:
        model = geospatialDatasets
        fields = ['dataset_names', 'dataset_types', 'file', 'crs', 'band_info']