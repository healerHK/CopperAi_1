
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import prospectivityProject, geospatialDatasets
from .forms import ProspectivityProjectForm, GeospatialDatasetForm

@login_required
def upload_view(request):
    datasets = geospatialDatasets.objects.filter(project__isnull=True)
    return render(request, 'prospectivity/upload.html', {'datasets': datasets})

@login_required
def upload_dataset(request):
    if request.method == 'POST':
        form = GeospatialDatasetForm(request.POST, request.FILES)
        if form.is_valid():
            dataset = form.save(commit=False)
            dataset.save()
        datasets = geospatialDatasets.objects.filter(project__isnull=True)
        return render(request, 'prospectivity/partials/upload_form.html', {'datasets': datasets})
    return redirect('upload')

@login_required
def project_view(request):
    projects = prospectivityProject.objects.all()
    return render(request, 'prospectivity/project.html', {'projects': projects})

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProspectivityProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user_updated = request.user
            project.save()
        projects = prospectivityProject.objects.all()
        return render(request, 'prospectivity/partials/project_form.html', {'projects': projects})
    return redirect('project')

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(prospectivityProject, id=project_id)
    return render(request, 'prospectivity/project_detail.html', {'project': project})

@login_required
def dataset_upload(request, project_id):
    project = get_object_or_404(prospectivityProject, id=project_id)
    if request.method == 'POST':
        form = GeospatialDatasetForm(request.POST, request.FILES)
        if form.is_valid():
            dataset = form.save(commit=False)
            dataset.project = project
            dataset.save()
        return render(request, 'prospectivity/partials/dataset_list.html', {'project': project})
    return redirect('project_detail', project_id=project_id)

@login_required
def map_view(request):
    return render(request, 'prospectivity/map.html')

@login_required
def help_view(request):
    return render(request, 'prospectivity/help.html')

def home(request):
    return render(request, 'base.html')