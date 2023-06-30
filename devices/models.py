from django.db import models
import uuid
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()
from asgiref.sync import async_to_sync


def get_all_device_date():
    channel_layer = get_channel_layer()
    res_list = []
    for data in Devices.objects.all().values("active_power_W",
                                             "meter_time"):
        res_list.append({
            "active_power_W": data["active_power_W"],
            "meter_time": data["meter_time"].strftime("%m/%d/%Y, %H:%M:%S"),
        }
        )
    async_to_sync(channel_layer.group_send)(
        'live_data',
        {
            'type': 'chat_message',
            'message': res_list,
            'latest_date': {"apparent_power_VA":Devices.objects.last().apparent_power_VA}
        }
    )


class Devices(models.Model):
    class Meta:
        db_table = "devices"

    public_id = models.BigIntegerField(editable=False, unique=True)
    name = models.CharField(max_length=255)
    meter_address = models.CharField(max_length=255)

    status = models.CharField(
        ([("Live", "Live"), ("Down", "Down")]),
        default="Live",
        max_length=10,
    )
    data_point = models.DateTimeField()
    average_current = models.FloatField()
    voltage = models.FloatField()
    active_power_W = models.FloatField()

    apparent_power_VA = models.FloatField()
    active_energy_Wh = models.FloatField()
    apparent_energy_VAh = models.FloatField()
    phase_current = models.FloatField()
    neutral_current = models.FloatField()
    frequency = models.FloatField()
    meter_time = models.DateTimeField()
    pf = models.FloatField()
    bg_color = models.CharField(max_length=255, default="")

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.public_id = uuid.uuid4().int >> 75
        if self.status == "Live":
            self.bg_color = "green"
        else:
            self.bg_color = "red"

        super(Devices, self).save(*args, **kwargs)
        get_all_device_date()

    def __str__(self):
        return self.bg_color
