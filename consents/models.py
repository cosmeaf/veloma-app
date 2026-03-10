import hashlib
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ConsentTerm(models.Model):

    slug = models.SlugField(unique=True)

    title = models.CharField(max_length=255)

    required = models.BooleanField(default=True)

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["slug"]

    def __str__(self):
        return f"{self.title} ({self.slug})"


class ConsentVersion(models.Model):

    term = models.ForeignKey(
        ConsentTerm,
        on_delete=models.CASCADE,
        related_name="versions"
    )

    version = models.CharField(max_length=50)

    content = models.TextField()

    document_hash = models.CharField(
        max_length=64,
        editable=False
    )

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("term", "version")
        ordering = ["-created_at"]

    def generate_hash(self):

        payload = f"{self.term.slug}|{self.version}|{self.content}"

        return hashlib.sha256(payload.encode()).hexdigest()

    def save(self, *args, **kwargs):

        self.document_hash = self.generate_hash()

        super().save(*args, **kwargs)

    def __str__(self):

        return f"{self.term.slug} v{self.version}"


class UserConsent(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    term = models.ForeignKey(
        ConsentTerm,
        on_delete=models.CASCADE
    )

    version = models.ForeignKey(
        ConsentVersion,
        on_delete=models.CASCADE
    )

    accepted = models.BooleanField(default=True)

    accepted_at = models.DateTimeField(auto_now_add=True)

    document_hash = models.CharField(max_length=64)

    ip = models.GenericIPAddressField()

    user_agent = models.TextField()

    country = models.CharField(max_length=120)

    city = models.CharField(max_length=120)

    asn = models.CharField(max_length=50)

    isp = models.CharField(max_length=120)

    is_proxy = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        unique_together = ("user", "version")

        ordering = ["-created_at"]

    def __str__(self):

        return f"{self.user_id} -> {self.term.slug} v{self.version.version}"