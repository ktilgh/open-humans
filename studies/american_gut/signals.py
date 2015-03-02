from django.db.models.signals import post_save
from django.dispatch import receiver

from data_import.signal_helpers import task_signal

from .models import Barcode, DataFile


@receiver(post_save, sender=Barcode)
def post_save_cb(sender, instance, created, raw, update_fields, **kwargs):
    """
    Initiate retrieval of the data corresponding to an American Gut barcode.
    """
    task_params = {
        'barcodes': [instance.value]
    }

    task_signal(instance, created, raw, task_params, DataFile)