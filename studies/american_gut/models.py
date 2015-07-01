from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.db import models

from common import fields
from data_import.models import BaseDataFile, DataRetrievalTask

from ..models import BaseStudyUserData


class UserData(BaseStudyUserData):
    """
    Represents the user data for one American Gut participant.
    """

    class Meta:
        verbose_name = 'American Gut user data'
        verbose_name_plural = verbose_name

    user = fields.AutoOneToOneField(settings.AUTH_USER_MODEL,
                                    related_name='american_gut')

    text_name = 'American Gut'
    href_connect = 'https://www.microbio.me/AmericanGut/authed/open-humans/'
    href_add_data = 'https://www.microbio.me/AmericanGut/authed/open-humans/'
    href_learn = 'http://americangut.org/'
    retrieval_url = reverse_lazy('studies:american-gut:request-data-retrieval')
    msg_add_data = ("We don't have any sample barcodes that we can add "
                    'data for. You can add barcodes through the American '
                    'Gut website.')

    def get_retrieval_params(self):
        barcodes = [barcode.value for barcode in
                    Barcode.objects.filter(user_data=self)]
        app_task_params = {'barcodes': barcodes}
        return app_task_params

    @property
    def msg_curr_data(self):
        barcodes = [b.value for b in Barcode.objects.filter(user_data=self)]
        return ('Current barcodes: %s. ' % ','.join(barcodes) +
                '<a href="%s">Go to American Gut</a> ' % self.href_add_data +
                'to add more.')

    @property
    def has_key_data(self):
        """
        Return false if key data needed for data retrieval is not present.
        """
        connected = self.is_connected
        if connected:
            barcodes = Barcode.objects.filter(user_data=self)
            if barcodes:
                return True
        return False


class Barcode(models.Model):
    """
    An American Gut sample barcode.
    """

    user_data = models.ForeignKey(UserData, related_name='barcodes')

    value = models.CharField(primary_key=True, max_length=64)


class DataFile(BaseDataFile):
    """
    Storage for an American Gut data file.
    """

    class Meta:
        verbose_name = 'American Gut data file'

    user_data = models.ForeignKey(UserData)
    task = models.ForeignKey(DataRetrievalTask,
                             related_name='datafile_american_gut')
    subtype = models.CharField(max_length=64,
                               default='microbiome-16S-and-surveys')

    def __unicode__(self):
        return '%s:%s:%s' % (self.user_data.user, 'american_gut', self.file)
