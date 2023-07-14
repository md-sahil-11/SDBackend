import random
import string
import uuid
from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError

import pypdf as pyPdf

from apps.users.models import User


class CustomBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=timezone.now)
    updated_at = models.DateTimeField(auto_now=timezone.now)

    class Meta:
        abstract = True


def generate_sharable_code():
    letters = string.ascii_lowercase
    code = ''.join(random.choice(letters) for i in range(16))
    return code


class Pdf(CustomBaseModel):
    title = models.CharField(max_length=120, null=True, blank=True)
    file = models.FileField(upload_to="files/", null=True, blank=True)
    created_by = models.ForeignKey(User, related_name="created_pdfs", on_delete=models.CASCADE)
    cover_image = models.ImageField(upload_to="images/", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    pages = models.IntegerField(default=0)
    size = models.IntegerField(default=0)
    sharable_code = models.CharField(max_length=120, db_index=True, unique=True, default=generate_sharable_code, editable=False)

    class Meta:
        ordering = ["-created_at"]

    def clean(self) -> None:
        # verifying file type
        try:
            pdf = pyPdf.PdfReader(self.file)
        except pyPdf.errors.PyPdfError:
            raise ValidationError('You must upload a valid PDF file')

        meta = pdf.metadata
        if not self.title :
            if meta.title:
                self.title = meta.title
            else:
                self.title = self.file.name.split("/")[-1].split(".")[0].upper()
        if not self.description:
            self.description = f"This pdf is uploaded by {self.created_by.name}"
        self.pages = len(pdf.pages)
        self.size = int(self.file.size)
        
        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class PdfMember(CustomBaseModel):
    pdf = models.ForeignKey(Pdf, related_name="members", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="pdfs", on_delete=models.CASCADE)
    is_creator = models.BooleanField(default=False)

    class Meta:
        unique_together = ["pdf", "user"]
        ordering = ["?"]


class Comment(CustomBaseModel):
    text = models.TextField()
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    pdf = models.ForeignKey(Pdf, related_name="comments", on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]


class CommentLike(CustomBaseModel):
    text_id = models.CharField(max_length=150, null=True, blank=True)
    user = models.ForeignKey(User, related_name="likes", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user", "text_id"]


class CommentReply(CustomBaseModel):
    text = models.TextField()
    comment = models.ForeignKey(Comment, related_name="replies", on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ["-created_at"]