from django.core.management.base import BaseCommand
from django.core.serializers import serialize
from servicios.models import ProductList, TypeService, OrderJob, OutputOJ, Income
import json
#python manage.py generate_database_json
class Command(BaseCommand):
    help = 'Genera un archivo JSON con los datos de la base de datos'

    def handle(self, *args, **options):
        self.stdout.write("Generando archivo JSON con los datos de la base de datos...")
        
        data = {}
        
        #- Serializar los datos de cada Tabla
        data['product_list'] = json.loads(serialize('json', ProductList.objects.all()))
        data['type_service'] = json.loads(serialize('json', TypeService.objects.all()))
        data['order_job'] = json.loads(serialize('json', OrderJob.objects.all()))
        data['output_oj'] = json.loads(serialize('json', OutputOJ.objects.all()))
        data['income'] = json.loads(serialize('json', Income.objects.all()))

        #- Escribir los datos en un archivo JSON
        with open('database_data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
        
        self.stdout.write(self.style.SUCCESS("Archivo JSON con los datos de la base de datos generado correctamente"))







