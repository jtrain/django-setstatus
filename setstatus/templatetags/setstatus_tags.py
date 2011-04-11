from django.contrib.contenttypes.models import ContentType
from django.template import Library

from setstatus.models import SetStatus

register = Library()

@register.filter(name='has_status')
def has_status(obj, statusname):
    """
    Returns true if the filtered oject has the status given in arg.

    the statusname must be the display text of the choice.
    e.g.
    SETSTATUS_CHOICES = (
            ("0", "LOW"),
    )

    statusname must be "LOW" not "0" for the example above.

    """
    obj_type = ContentType.objects.get_for_model(obj)
    statuses = SetStatus.objects.filter(content_type__pk=obj_type.id,
                                      object_id=obj.id)
    active_status = filter(lambda s: s.active(), statuses)

    return any(filter(
                lambda s: s.get_status_display() == statusname,
                active_status
           )
    )
