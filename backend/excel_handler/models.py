from django.db import models
import uuid
from django.utils import timezone

# Create your models here.

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def all_with_deleted(self):
        return super().get_queryset()

    def deleted_only(self):
        return super().get_queryset().filter(is_active=False)

class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager() 

    class Meta:
        abstract = True
    
    def delete(self, using=None):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save(using=using)

    def restore(self):
        self.is_active = True
        self.deleted_at = None
        self.save()

class ExcelFile(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_id = models.CharField(max_length=100, unique=True)
    original_filename = models.CharField(max_length=255)
    upload_path = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_filename

class ExcelVersion(BaseModel):
    file = models.ForeignKey(ExcelFile, on_delete=models.CASCADE, related_name="versions")
    version_number = models.PositiveIntegerField()
    dataframe_json = models.JSONField()  # Stores the full DataFrame

    class Meta:
        unique_together = ('file', 'version_number')
        ordering = ['-version_number']

class ExcelOperationLog(BaseModel):
    version = models.ForeignKey(ExcelVersion, on_delete=models.CASCADE, related_name="operations")
    operation_type = models.CharField(max_length=50)  # e.g., add_column, filter_rows
    description = models.TextField()  # Optional prompt or explanation
    performed_at = models.DateTimeField(auto_now_add=True)
