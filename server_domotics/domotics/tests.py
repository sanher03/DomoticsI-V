from django.test import TestCase
from django.core.management import call_command

from devices.models import Device
from rules.models import Rule


class DemoSeedCommandTests(TestCase):
    def test_creates_example_devices_and_rules_once(self):
        call_command("seed_demo")

        self.assertEqual(
            list(Device.objects.order_by("id").values_list("id", "type")),
            [(101, "SWITCH"), (102, "SENSOR"), (103, "CLOCK")],
        )
        self.assertEqual(Rule.objects.count(), 3)

        Device.objects.filter(id=101).update(name="Customized switch")
        call_command("seed_demo")

        self.assertEqual(Device.objects.get(id=101).name, "Customized switch")
        self.assertEqual(Rule.objects.count(), 3)
