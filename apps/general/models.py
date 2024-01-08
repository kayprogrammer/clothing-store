from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class SiteDetail(BaseModel):
    name = models.CharField(max_length=200, default="Clothing Store")
    desc = models.TextField(
        default="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum"
    )
    email = models.EmailField(default="kayprogrammer1@gmail.com")
    phone = models.CharField(max_length=20, default="+2348133831036")
    address = models.CharField(max_length=500, default="23, Lagos, Nigeria")
    work_hours = models.CharField(max_length=500, default="09:00 - 17:00")
    maps_url = models.URLField(
        default="https://maps.google.com/maps?q=Av.+L%C3%BAcio+Costa,+Rio+de+Janeiro+-+RJ,+Brazil&t=&z=13&ie=UTF8&iwloc=&output=embed"
    )

    fb = models.URLField(verbose_name=_("Facebook"), default="https://www.facebook.com")
    ig = models.URLField(
        verbose_name=_("Instagram"), default="https://www.instagram.com/"
    )
    tw = models.URLField(verbose_name=_("Twitter"), default="https://www.twitter.com/")
    ln = models.URLField(
        verbose_name=_("Linkedin"), default="https://www.linkedin.com/"
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self._state.adding and SiteDetail.objects.exists():
            raise ValidationError(_("Only one site detail object can be created."))
        return super(SiteDetail, self).save(*args, **kwargs)


ROLE_CHOICES = (
    ("CO-Founder", "CO-Founder"),
    ("Product Expert", "Product Expert"),
    ("Chief Marketing", "Chief Marketing"),
    ("Product Specialist", "Product Specialist"),
    ("Product Photographer", "Product Photographer"),
    ("General Manager", "General Manager"),
)


class TeamMember(BaseModel):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200, choices=ROLE_CHOICES)
    desc = models.CharField(max_length=300)
    avatar = models.ImageField(upload_to="team/")
    fb = models.URLField(verbose_name=_("Facebook"), default="https://www.facebook.com")
    ig = models.URLField(
        verbose_name=_("Instagram"), default="https://www.instagram.com/"
    )
    tw = models.URLField(verbose_name=_("Twitter"), default="https://www.twitter.com/")
    ln = models.URLField(
        verbose_name=_("Linkedin"), default="https://www.linkedin.com/"
    )

    def __str__(self):
        return self.name

    @property
    def avatar_url(self):
        try:
            url = self.avatar.url
        except:
            url = ""
        return url


class Message(BaseModel):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    text = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at"]
