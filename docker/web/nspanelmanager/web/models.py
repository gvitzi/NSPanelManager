from requests.models import default_hooks
from django.db import models
from datetime import datetime
import django.utils


class Settings(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class NSPanelSettings(models.Model):
    nspanel = models.ForeignKey("NSPanel", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self) -> str:
        return F"{self.nspanel.friendly_name}::{self.name}"


class Room(models.Model):
    # Get the next free number in the ordering
    def number():
        no = Room.objects.all().count()
        if no == None:
            return 1
        else:
            return no + 1

    friendly_name = models.CharField(max_length=30)
    displayOrder = models.IntegerField(default=number)

    def __str__(self) -> str:
        return self.friendly_name


def _default_nspanel_status_data():
    return {
        "rssi": 0,
        "mac": "??:??:??:??:??:??",
        "free_heap": 0
    }


class NSPanel(models.Model):
    mac_address = models.CharField(max_length=17)
    friendly_name = models.CharField(max_length=100)
    last_seen = models.DateTimeField(default=django.utils.timezone.now)
    ip_address = models.CharField(max_length=15, default="")
    version = models.CharField(max_length=15, default="")
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    wifi_rssi = models.IntegerField(default=0)
    heap_used_pct = models.IntegerField(default=0)
    temperature = models.FloatField(default=0)
    online_state = models.BooleanField(default=False)
    button1_mode = models.IntegerField(default=0)
    button1_detached_mode_light = models.ForeignKey("Light", on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    button2_mode = models.IntegerField(default=0)
    button2_detached_mode_light = models.ForeignKey("Light", on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    md5_firmware = models.CharField(max_length=64, default="")
    md5_data_file = models.CharField(max_length=64, default="")
    md5_tft_file = models.CharField(max_length=64, default="")
    def __str__(self) -> str:
        return self.friendly_name


class Light(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    friendly_name = models.CharField(max_length=255, default="")
    # "home_assistant", "openhab" or "manual"
    type = models.CharField(max_length=16, default="manual")
    is_ceiling_light = models.BooleanField(default=False)
    can_dim = models.BooleanField(default=False)
    can_rgb = models.BooleanField(default=False)
    can_color_temperature = models.BooleanField(default=False)
    home_assistant_name = models.CharField(max_length=255, default="")
    openhab_name = models.CharField(max_length=255, default="")
    openhab_control_mode = models.CharField(max_length=32, default="dimmer")
    openhab_item_switch = models.CharField(max_length=255, default="")
    openhab_item_dimmer = models.CharField(max_length=255, default="")
    openhab_item_color_temp = models.CharField(max_length=255, default="")
    openhab_item_rgb = models.CharField(max_length=255, default="")
    room_view_position = models.IntegerField(default=0)

    def __str__(self) -> str:
        return F"{self.room.friendly_name} -> {self.friendly_name}"

class Scene(models.Model):
    friendly_name = models.CharField(max_length=32)
    room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.CASCADE)

class LightState(models.Model):
    light = models.ForeignKey(Light, on_delete=models.CASCADE)
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE)
    color_mode = models.CharField(max_length=32, default="dimmer")
    light_level = models.IntegerField(default=0)
    color_temperature = models.IntegerField(default=4000)
    hue = models.IntegerField(default=0)
    saturation = models.IntegerField(default=0)
