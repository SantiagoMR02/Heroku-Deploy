from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib import messages #Parra lso mensajes de autentificación 
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate #Nos permite autentificar a un usuario y si existe en la base de datos.

from django.contrib.auth.models import User

from django.views import View

#PDF
import os
from xhtml2pdf import pisa
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.template.loader import get_template
from django.contrib.staticfiles import finders
from django.urls import reverse_lazy

from inventario.models import Inventory
from actividades.models import Activity
from gestionHumana.models import Salary
from .forms import RegisterForm
#apartado de pagos 
from servicios.models import DEFAULT_CATEGORY_STATES, DEFAULT_STATES, TypeService, Income, OrderJob, ProductList
from servicios.forms import OrderJobForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
#correos
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import render

def index(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        
        template = render_to_string('email_template.html', {
            'name': name,
            'email': email,
            'message': message
        })
    
        email = EmailMessage(
            subject,
            template,
            settings.EMAIL_HOST_USER,
            ['vs157918@gmail.com',]
        )
    
        email.fail_silently = False
        email.send()
    
        return render(request, 'index.html', {})

    return render(request, 'index.html', {
        'message': 'Listado de Productos',
        'title': 'Productos',
        'products': [
            {'title': 'Playera', 'price': 5, 'stock': True},
            {'title': 'Pantalon', 'price': 10, 'stock': True},
            {'title': 'Zapatos Jordan NIKE', 'price': 105, 'stock': False},
        ]
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if user.is_superuser:
                return redirect('admin:index')
            else:
                messages.success(request, 'Bienvenido {}'.format(user.username))
                return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña no válidos')

    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    messages.success(request,'Sesión cerrada de manera exitosa')
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = RegisterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():

        user = form.save()
        if user:
            login(request,user)
            messages.success(request, 'Usuario creado de manera exitosa')
            return redirect('index')

    return render(request,'users/register.html',{
        'form':form 
    })


def remember_view (request):
    return render(request, 'users/remember.html',{
        
    })

def pruevas (request):
    return render(request, 'pruevas.html',{
        
    })

def pagos(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    incomes = Income.objects.all()
    services = TypeService.objects.all()

    if request.method == 'POST':
        form = OrderJobForm(request.POST)
        if form.is_valid():
            # Crear instancias de los modelos relacionados
            product_list = ProductList.objects.create(
                amount=request.POST["amount"],
                description=request.POST["description"],
                status=request.POST["status"],
                category=request.POST["category"]
            )
            type_service = TypeService.objects.get(id=request.POST["typeService"])
            income = Income.objects.get(id=request.POST["paymentMethod"])
            
            # Crear instancia de OrderJob y guardarla en la base de datos
            ot = OrderJob.objects.create(
                nombre_cliente=request.POST["nombre_cliente"],
                numberPhone=request.POST["numberPhone"],
                dateOT=request.POST["dateOT"],
                productList=product_list,
                typeService=type_service,
                paymentMethod=income
            )
            ot.save()  # Guardar la instancia de OrderJob
            messages.success(request, 'Producto agregado')
            return redirect('index')
    else:
        form = OrderJobForm()
        print(form.errors)
        
    today = timezone.now().date()  # Obtener la fecha actual
    context = {
        'status': DEFAULT_STATES,
        'category': DEFAULT_CATEGORY_STATES,
        'typeService': services,
        'form': form,
        'incomes': incomes,
        'today': today  # Pasar la fecha actual al contexto de la plantilla
    }
    return render(request, 'pagos.html', context)
#PDf views
class PDFinve(View):

    def link_callback(self, uri, rel):
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL       
                    sRoot = settings.STATIC_ROOT     
                    mUrl = settings.MEDIA_URL       
                    mRoot = settings.MEDIA_ROOT      

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            if not os.path.isfile(path):
                    raise RuntimeError(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path
    
    def get(self, request, *args, **kwargs):
        try:
            inventarios = Inventory.objects.all()  
            template = get_template('PDF/PDFinve.html')
            context = {
                'inventarios': inventarios
            }

            html = template.render(context)
            
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="Reporte Invetario.pdf"'
            pisa_status = pisa.CreatePDF(
                 html, dest=response,
                 link_callback=self.link_callback
                 )
         
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            
            return response
        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse('Error al generar el PDF')
        

class PDFacti(View):
    def link_callback(self, uri, rel):
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL       
                    sRoot = settings.STATIC_ROOT     
                    mUrl = settings.MEDIA_URL       
                    mRoot = settings.MEDIA_ROOT      

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            if not os.path.isfile(path):
                    raise RuntimeError(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path
    
    def get(self, request, *args, **kwargs):
        try:
            actividades = Activity.objects.all()  
            template = get_template('PDF/PDFacti.html')
            context = {
                'actividades': actividades
            }

            html = template.render(context)
            
            response = HttpResponse(content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="reporte de actividades.pdf"'
            pisa_status = pisa.CreatePDF(
                 html, dest=response,
                 link_callback=self.link_callback
                 )
         
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            
            return response
        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse('Error al generar el PDF')

class PDFsal(View):
    def link_callback(self, uri, rel):
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL       
                    sRoot = settings.STATIC_ROOT     
                    mUrl = settings.MEDIA_URL       
                    mRoot = settings.MEDIA_ROOT      

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            if not os.path.isfile(path):
                    raise RuntimeError(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path
    
    def get(self, request, *args, **kwargs):
        try:
            salarios = Salary.objects.all()  
            template = get_template('PDF/PDFsal.html')
            context = {
                'salarios': salarios
            }

            html = template.render(context)
            
            response = HttpResponse(content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="Reporte Nomina Empleados.pdf"'
            pisa_status = pisa.CreatePDF(
                 html, dest=response,
                 link_callback=self.link_callback
                 )
         
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            
            return response
        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse('Error al generar el PDF')
        
class PDFot (View):
    def link_callback(self, uri, rel):
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL       
                    sRoot = settings.STATIC_ROOT     
                    mUrl = settings.MEDIA_URL       
                    mRoot = settings.MEDIA_ROOT      

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            if not os.path.isfile(path):
                    raise RuntimeError(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path
    
    def get(self, request, *args, **kwargs):
        try:
            ordenesTrabajo = OrderJob.objects.all()  
            template = get_template('PDF/PDFot.html')
            context = {
                'ordenesTrabajo': ordenesTrabajo
            }

            html = template.render(context)
            
            response = HttpResponse(content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="Reporte Ordenes de Trabajo.pdf"'
            pisa_status = pisa.CreatePDF(
                 html, dest=response,
                 link_callback=self.link_callback
                 )
         
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            
            return response
        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse('Error al generar el PDF')
        