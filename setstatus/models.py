from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

import datetime

CHOICES = getattr(settings, 'SETSTATUS_CHOICES',
                        [('0', _('LOW'   )),
                         ('1', _('MEDIUM')),
                         ('2', _('HIGH'  ))] )

MAXLEN = getattr(settings, 'SETSTATUS_MAXLEN_CHARFIELD', 255)
                            

class SetStatus(models.Model):
    """
    The core set status model.

    """
    status = models.CharField(
                       verbose_name=_("Status"),
                       max_length=MAXLEN,
                       choices=CHOICES)

    start_at = models.DateTimeField(
                        verbose_name=_("Start at"),
                        help_text=_('Apply status from this date.'))

    end_at = models.DateTimeField(
                        verbose_name=_("End at"),
                        default=datetime.datetime(2099, 12, 31),
                        help_text=_('Remove status this date.'))

    # who are we attached to.
    object_id = models.IntegerField(verbose_name=_('Object id'))
    content_type = models.ForeignKey(
                        ContentType,
                        verbose_name=_('Content type'),
                        related_name="%(app_label)s_%(class)s_setstatus_items"
                   )
    content_object = GenericForeignKey()

    # user that modified this record.
    modified_by = models.ForeignKey(User)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
                            
    def active(self):
        """
        Returns True if this record is between the start_at and end_at dates.

        """
        now = datetime.datetime.now()
        return self.start_at < now and now < self.end_at
    active.boolean = True


    class Meta:
        verbose_name = _("Status")
        verbose_name_plural = _("Statuses")
