from django.contrib import admin
from .models import Organization, Project

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'atlas_id', 'created_at']
    search_fields = ['name', 'atlas_id']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'atlas_id', 'created_at']
    search_fields = ['name', 'atlas_id']
    list_filter = ['organization']
    readonly_fields = ['created_at', 'updated_at']
