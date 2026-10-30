from django.core.management.base import BaseCommand
from django.db import transaction

from devices.models import Device
from rules.models import Rule


class Command(BaseCommand):
    help = "Create example devices and rules for a fresh demo database."

    @transaction.atomic
    def handle(self, *args, **options):
        if Device.objects.exists():
            self.stdout.write("Devices already exist; keeping the current database.")
            return

        switch = Device.objects.create(
            id=101, name="Interruptor de demostración", type="SWITCH"
        )
        sensor = Device.objects.create(
            id=102, name="Sensor de demostración", type="SENSOR"
        )
        clock = Device.objects.create(
            id=103, name="Reloj de demostración", type="CLOCK"
        )

        Rule.objects.create(
            name="Encender por temperatura alta",
            device1=sensor,
            comparator="MORE_THAN",
            value="20",
            device2=switch,
            turn_on=True,
        )
        Rule.objects.create(
            name="Apagar por temperatura baja",
            device1=sensor,
            comparator="LESS_THAN",
            value="15",
            device2=switch,
            turn_on=False,
        )
        Rule.objects.create(
            name="Apagar a las 09:00:10",
            device1=clock,
            comparator="EQUALS",
            value="09:00:10",
            device2=switch,
            turn_on=False,
        )

        self.stdout.write(self.style.SUCCESS("Created demo devices and rules."))
