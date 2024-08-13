import uuid
from django.core.management.base import BaseCommand
from django_seed import Seed
from django.utils import timezone
from sensors.models import PressureSensor, PressureReading
from my_tags.models import Tag

class Command(BaseCommand):
    help = 'Seed the database with PressureSensor and PressureReading data'

    def add_arguments(self, parser):
        parser.add_argument('--number', type=int, help='Number of records to seed')

    def handle(self, *args, **options):
        number = options.get('number', 10)  
        seeder = Seed.seeder()
       
        seeder.add_entity(PressureSensor, number, {
            'serial_number': lambda x: str(uuid.uuid4()),  
            'created_at': lambda x: timezone.now(),
            'updated_at': lambda x: timezone.now(),
        })

        seeder.add_entity(PressureReading, number, {
            'timestamp': lambda x: timezone.now(),
        })

        inserted_pks = seeder.execute()

        tags = Tag.objects.all()
        sensors = PressureSensor.objects.filter(pk__in=inserted_pks[PressureSensor])
        readings = PressureReading.objects.filter(pk__in=inserted_pks[PressureReading])

        for sensor in sensors:
            sensor.tags.add(*tags)

        for reading in readings:
            reading.tags.add(*tags)

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {number} PressureSensors and PressureReadings.'))
