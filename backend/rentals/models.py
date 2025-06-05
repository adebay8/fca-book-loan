from django.db import models

from librarysystem.models import BaseTimeStampedModel

class Rental(BaseTimeStampedModel):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    book_item = models.ForeignKey("catalog.BookItem", on_delete=models.CASCADE)
    returned_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def is_active(self):
        return self.returned_at is None