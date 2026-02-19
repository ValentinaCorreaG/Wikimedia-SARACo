from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class TeamArea(models.Model):
    """Team area for organizing users by department or project area."""
    text = models.CharField(
        _("Name"),
        max_length=420,
        help_text=_("Human-readable name of the team area")
    )
    code = models.CharField(
        _("Code"),
        max_length=50,
        unique=True,
        help_text=_("Short identifier of the team area")
    )

    class Meta:
        verbose_name = _("Team area")
        verbose_name_plural = _("Team areas")
        ordering = ['text']

    def __str__(self):
        return self.text


class Position(models.Model):
    """User position within a team area."""
    text = models.CharField(
        _("Name"),
        max_length=420,
        help_text=_("Human-readable name of the position")
    )
    type = models.ForeignKey(
        Group,
        on_delete=models.PROTECT,
        verbose_name=_("Permission group"),
        help_text=_("The permission group this position belongs to")
    )
    area_associated = models.ForeignKey(
        TeamArea,
        on_delete=models.PROTECT,
        related_name="positions",
        verbose_name=_("Team Area"),
        help_text=_("The team area this position belongs to")
    )

    class Meta:
        verbose_name = _("Position")
        verbose_name_plural = _("Positions")
        ordering = ['text']
        unique_together = (("area_associated", "text"),)

    def __str__(self):
        return self.text


class UserProfile(models.Model):
    """Extended user profile with Wikimedia and social information."""
    
    class GenderChoices(models.TextChoices):
        MALE = "male", _("Male")
        FEMALE = "female", _("Female")
        NON_BINARY = "non_binary", _("Non Binary")
        OTHER = "other", _("Other")
        NOT_DECLARED = "not_declared", _("Not declared")

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name=_("User"),
        help_text=_("The user which this profile's about")
    )
    
    # Wikimedia information
    professional_wiki_handle = models.CharField(
        _("Professional username"),
        max_length=50,
        blank=True,
        default=""
    )
    personal_wiki_handle = models.CharField(
        _("Personal username"),
        max_length=50,
        blank=True,
        default=""
    )
    
    # Personal information
    gender = models.CharField(
        _("Gender"),
        max_length=20,
        choices=GenderChoices.choices,
        blank=True,
        default=GenderChoices.NOT_DECLARED
    )
    photograph = models.CharField(
        _("Photograph filename"),
        max_length=420,
        blank=True,
        default=""
    )
    
    # Organization information
    position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        related_name="users",
        null=True,
        blank=True,
        verbose_name=_("Position"),
        help_text=_("The position this user belongs to")
    )
    
    # Social media
    twitter = models.CharField(
        _("Twitter"),
        max_length=100,
        blank=True,
        default="",
        help_text=_("Twitter handle")
    )
    facebook = models.CharField(
        _("Facebook"),
        max_length=100,
        blank=True,
        default="",
        help_text=_("Facebook handle")
    )
    instagram = models.CharField(
        _("Instagram"),
        max_length=100,
        blank=True,
        default="",
        help_text=_("Instagram handle")
    )
    
    # Academic identifiers
    wikidata_item = models.CharField(
        _("Wikidata item"),
        max_length=100,
        blank=True,
        default="",
        help_text=_("Wikidata QID")
    )
    linkedin = models.CharField(
        _("LinkedIn"),
        max_length=100,
        blank=True,
        default="",
        help_text=_("LinkedIn handle")
    )
    orcid = models.CharField(
        _("ORCID"),
        max_length=100,
        blank=True,
        default="",
        help_text=_("ORCID ID")
    )

    class Meta:
        verbose_name = _("User profile")
        verbose_name_plural = _("User profiles")

    def __str__(self):
        return self.professional_wiki_handle or self.user.first_name or self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Creation and association of a user profile to the user upon first login.
    """
    if created:
        UserProfile.objects.create(user=instance)
