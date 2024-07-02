from .decorators import administracion_required, gestores_tramites_required,all_required 
from secretaria_docente.correo import enviar_correo_cambio_estado
from django.contrib.auth.decorators import login_required
from atencion_poblacion.forms import CambiarEstadoForm
from django.utils.decorators import method_decorator
from usuarios.forms import InformacionPersonalForm
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from django.contrib.auth.models import Group
from django.http.request import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from usuarios.models import Usuario
from django.contrib import messages
from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone
from .choices import Estado
from.models import Tramite
import json, calendar

from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
    )

User = get_user_model()


# Create your views here
def Main(request):
    return render(request, 'main.html')

@method_decorator([login_required, administracion_required ], name='dispatch')
class Tramites_All(ListView):
    model = Tramite
    template_name = 'General/tramites_all.html'
    context_object_name = 'tramites'

@login_required
@administracion_required
def Tramites_Delete_Tramites_All(request,id):
    tramite = Tramite.objects.get(id=id)
    tramite.delete()
    return redirect("Tramites_All")


# Administracion
@login_required
@administracion_required
def Cambiar_Gestor(request, id): 
    if request.method == 'POST':
        try:
            usuario = Usuario.objects.get(id=id)
        except Usuario.DoesNotExist:
            return render (request,"plataforma/Atención a la Poblacion.html",{'response':'incorrecto', 'message':'Usuario no encontrado'})

        group_names = list(Group.objects.all().values_list('name', flat=True)) 
        selected_group = request.POST['role']

        if selected_group in group_names:
            try:
                group = Group.objects.get(name=selected_group)
            except Group.DoesNotExist:
                return render (request,"plataforma/Atención a la Poblacion.html",{'response':'incorrecto', 'message':'Grupo no encontrado'})

            usuario.groups.clear()
            usuario.groups.add(group)
            return redirect('Gestores')
        else:
           return render (request,"plataforma/Atención a la Poblacion.html",{'response':'incorrecto', 'message':'Rol inválido'})
    else:
        group_names = list(Group.objects.all().values_list('name', flat=True))
        return render(request, "General/cambiar_gestor.html", {'group_names': group_names})


@login_required
@administracion_required
def Gestores(request):
    context = {
        'usuarios': Usuario.objects.all()
    }
    return render (request,"General/gestores.html", context)
    
@login_required
@all_required
def Sitio_Administrativo(request):
    usuarios_count =  Usuario.objects.all().count()
    cantidad_tramites = Tramite.objects.all().count()
    tramite_t =Tramite.objects.all() 

    pregrado_nacional = Tramite.objects.filter(tipo_estudio='Pregrado', uso= 'Nacional') 
    pregrado_internacional = Tramite.objects.filter(tipo_estudio='Pregrado', uso_i='Internacional') 
    posgrado_nacional = Tramite.objects.filter(tipo_est='Posgrado', uso='Nacional')  
    posgrado_internacional = Tramite.objects.filter(tipo_est='Posgrado', uso_i='Internacional') 
    # Contamos los trámites para cada categoría
    pregrado_nacional_count = pregrado_nacional.count()
    pregrado_internacional_count = pregrado_internacional.count()
    posgrado_nacional_count = posgrado_nacional.count()
    posgrado_internacional_count = posgrado_internacional.count()
    
    
    data_grafica = [
        {'categoria': 'Pregrado Nacional', 'cantidad': pregrado_nacional_count},
        {'categoria': 'Pregrado Internacional', 'cantidad': pregrado_internacional_count},
        {'categoria': 'Posgrado Nacional', 'cantidad': posgrado_nacional_count},
        {'categoria': 'Posgrado Internacional', 'cantidad': posgrado_internacional_count}
    ]
    # Convertimos los datos a JSON para pasarlos al template
    data_json = json.dumps(data_grafica)

    #Grafica Estados
    estados_tramites = Tramite.objects.values('estado').annotate(frecuencia=Count('estado'))
   
    estados_validos = [item[0] for item in Estado]
    # Filtra los resultados para incluir solo los estados válidos
    estados_filtrados = {estado['estado']: estado['frecuencia'] for estado in estados_tramites if estado['estado'] in estados_validos}
    data_grafica_estados = [{'nombre': estado, 'valor': frecuencia} for estado, frecuencia in estados_filtrados.items()]
    data_json_estados = json.dumps(data_grafica_estados)
    
    completados = Tramite.objects.filter(estado='Completado').count()
    espera = Tramite.objects.filter(estado='En Espera').count()
    context ={
        'tramite_t': tramite_t,
        'cantidad_tramites' : cantidad_tramites,
        'usuarios_count': usuarios_count,
        'completado': completados,
        'espera': espera,
        'data_grafica': data_json,
        'data_grafica_estados': data_json_estados,
    }
    if request.user.groups.filter(name='Administrador de Módulo').exists():
        return render (request,"General/sitio_administrativo.html", context)
    elif request.user.groups.filter(name='Gestor General SD').exists():
        return render (request,"General/sitio_administrativo.html", context)
    elif request.user.groups.filter(name='Gestores de Trámites SD').exists():
        return render (request,"General/sitio_administrativo.html", context)
    
    return render(request, "General/sitio_administrativo.html",context) 

@login_required
@administracion_required
def Graficas(request):
    #Grafica Completados
    tramites_completados = Tramite.objects.filter(estado='Completado')

    # Contamos los trámites completados para cada categoría
    pregrado_nacional_completados_count = tramites_completados.filter(tipo_estudio='Pregrado', uso='Nacional').count()
    pregrado_internacional_completados_count = tramites_completados.filter(tipo_estudio='Pregrado', uso_i='Internacional').count()
    posgrado_nacional_completados_count = tramites_completados.filter(tipo_est='Posgrado', uso='Nacional').count()
    posgrado_internacional_completados_count = tramites_completados.filter(tipo_est='Posgrado', uso_i='Internacional').count()

    print(pregrado_nacional_completados_count)
    print(pregrado_internacional_completados_count)
    print(posgrado_nacional_completados_count)
    print(posgrado_internacional_completados_count)

    # Preparamos los datos para la gráfica
    data_grafica_completados = [
        {'categoria': 'Pregrado Nacional Completados', 'cantidad': pregrado_nacional_completados_count},
        {'categoria': 'Pregrado Internacional Completados', 'cantidad': pregrado_internacional_completados_count},
        {'categoria': 'Posgrado Nacional Completados', 'cantidad': posgrado_nacional_completados_count},
        {'categoria': 'Posgrado Internacional Completados', 'cantidad': posgrado_internacional_completados_count}
    ]
    
    # Convertimos los datos a JSON para pasarlos al template
    data_json_completados = json.dumps(data_grafica_completados)


     # Obtener los gestores relevantes
    gestores_relevantes = Gestor.objects.filter(nombre__in=['Nombre Gestor 1', 'Nombre Gestor 2'])  # Reemplaza 'Nombre Gestor 1', 'Nombre Gestor 2' con los nombres reales de tus gestores o filtra por grupo como antes
    
    # Preparar los datos para la gráfica
    data_grafica_por_gestor_y_mes = []
    
    for gestor in gestores_relevantes:
        for mes in range(1, 13):  # Los meses van de 1 (enero) a 12 (diciembre)
            tramites_por_mes = Tramite.objects.filter(gestor=gestor, estado='Completado', fecha__month=mes).aggregate(count=Count('id'))['count'] or 0
            data_grafica_por_gestor_y_mes.append({
                'nombre': f"{gestor.nombre} - {calendar.month_name[mes]}",
                'tramites_procesados': tramites_por_mes
            })
    
    # Convertir los datos a JSON para pasarlos al template
    data_json = json.dumps(data_grafica_por_gestor_y_mes)
    
    return render(request, "General/grafica.html", {
        'data_grafica_por_gestor_y_mes': data_json,
    })

    return render(request, "General/grafica.html", {
        'data_grafica_completados': data_json_completados,
       
    })

@login_required
@administracion_required
@gestores_tramites_required
def Cambiar_Estado(request, id):
    tramite = Tramite.objects.get(id=id)
    if request.POST:
        try:
            tramite.estado = request.POST["role"]
            enviar_correo_cambio_estado(tramite)
            tramite.save()
            return redirect("Tramites_All")
        except Exception as e:
            messages.error(request, "Algo salió mal con el envío del correo, por favor intentelo de nuevo")
            print(e)
            return render(request, "General/cambiar_estado.html")
    
    form = CambiarEstadoForm(instance=tramite)
    estados = [e[0] for e in Estado]
    return render(request,"General/cambiar_estado.html",{"form":form, "estados":estados})

@login_required
@gestores_tramites_required
def Tramites_Tipo_Pregrado(request):
    # Filtrando trámites donde 'tipo_estudio' es verdadero
    tramites_pregrado = Tramite.objects.filter(tipo_estudio='Pregrado')    
    context ={'tramites_pregrado': tramites_pregrado,}
    return render(request, 'General/tramite_tipo_pregrado.html', context)

@login_required
@gestores_tramites_required
def Tramites_Delete_Tramites_Tipo_Pregrado(request,id):
    tramite = Tramite.objects.get(id=id)
    tramite.delete()
    return redirect("Tramites_Tipo_Pregrado")

@method_decorator([login_required, gestores_tramites_required ], name='dispatch')
class Tramites_Detail_Pregrado(DetailView):
    model = Tramite
    template_name = "General/tramites_detail_pregrado.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tramite = self.get_object()

        #Variables para controlar qué formularios mostrar
        context['Pregrado_Nacional'] = tramite.tipo_pren and tramite.tipo_pren.strip()!= ''
        context['Pregrado_Nacional_Legalizacion'] = (tramite.tipo_estudio and tramite.uso and tramite.legalizacion) and tramite.tipo_estudio.strip()!= '' and tramite.uso.strip()!= ''
        context['Pregrado_Internacional'] = tramite.tipo_prei and tramite.tipo_prei.strip()!= ''
        context['Pregrado_Internacional_Legalizacion'] = (tramite.tipo_estudio and tramite.uso_i and tramite.legalizacion) and tramite.tipo_estudio.strip()!= '' and tramite.uso_i.strip()!= ''
        context['Posgrado_Nacional'] = tramite.tipo_posn and tramite.tipo_posn.strip()!= ''
        context['Posgrado_Nacional_Legalizacion'] = (tramite.tipo_est and tramite.uso and tramite.legalizacion) and tramite.tipo_est.strip()!= '' and tramite.uso.strip()!= ''
        context['Posgrado_Internacional'] = tramite.tipo_posi and tramite.tipo_posi.strip()!= ''
        context['Posgrado_Internacional_Legalizacion'] = (tramite.tipo_est and tramite.uso_i and tramite.legalizacion) and tramite.tipo_est.strip()!= '' and tramite.uso_i.strip()!= ''
        return context




@login_required
@gestores_tramites_required
def Tramites_Tipo_Posgrado(request):
    tramites_posgrado = Tramite.objects.filter(tipo_est='Posgrado')    
    context ={'tramites_posgrado': tramites_posgrado,}
    return render(request, 'General/tramite_tipo_posgrado.html', context)

@login_required
@gestores_tramites_required
def Tramites_Delete_Tramites_Tipo_Posgrado(request,id):
    tramite = Tramite.objects.get(id=id)
    tramite.delete()
    return redirect("Tramites_Tipo_Posgrado")

@method_decorator([login_required, gestores_tramites_required ], name='dispatch')
class Tramites_Detail_Posgrado(DetailView):
    model = Tramite
    template_name = "General/tramites_detail_posgrado.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tramite = self.get_object()

        #Variables para controlar qué formularios mostrar
        context['Pregrado_Nacional'] = tramite.tipo_pren and tramite.tipo_pren.strip()!= ''
        context['Pregrado_Nacional_Legalizacion'] = (tramite.tipo_estudio and tramite.uso and tramite.legalizacion) and tramite.tipo_estudio.strip()!= '' and tramite.uso.strip()!= ''
        context['Pregrado_Internacional'] = tramite.tipo_prei and tramite.tipo_prei.strip()!= ''
        context['Pregrado_Internacional_Legalizacion'] = (tramite.tipo_estudio and tramite.uso_i and tramite.legalizacion) and tramite.tipo_estudio.strip()!= '' and tramite.uso_i.strip()!= ''
        context['Posgrado_Nacional'] = tramite.tipo_posn and tramite.tipo_posn.strip()!= ''
        context['Posgrado_Nacional_Legalizacion'] = (tramite.tipo_est and tramite.uso and tramite.legalizacion) and tramite.tipo_est.strip()!= '' and tramite.uso.strip()!= ''
        context['Posgrado_Internacional'] = tramite.tipo_posi and tramite.tipo_posi.strip()!= ''
        context['Posgrado_Internacional_Legalizacion'] = (tramite.tipo_est and tramite.uso_i and tramite.legalizacion) and tramite.tipo_est.strip()!= '' and tramite.uso_i.strip()!= ''
        return context

@method_decorator([login_required, gestores_tramites_required ], name='dispatch')
class Tramites_Detail_Admin(DetailView):
    model = Tramite
    template_name = "General/tramites_detail_admin.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tramite = self.get_object()

        #Variables para controlar qué formularios mostrar
        context['Pregrado_Nacional'] = tramite.tipo_pren and tramite.tipo_pren.strip()!= ''
        context['Pregrado_Nacional_Legalizacion'] = (tramite.tipo_estudio and tramite.uso and tramite.legalizacion) and tramite.tipo_estudio.strip()!= '' and tramite.uso.strip()!= ''
        context['Pregrado_Internacional'] = tramite.tipo_prei and tramite.tipo_prei.strip()!= ''
        context['Pregrado_Internacional_Legalizacion'] = (tramite.tipo_estudio and tramite.uso_i and tramite.legalizacion) and tramite.tipo_estudio.strip()!= '' and tramite.uso_i.strip()!= ''
        context['Posgrado_Nacional'] = tramite.tipo_posn and tramite.tipo_posn.strip()!= ''
        context['Posgrado_Nacional_Legalizacion'] = (tramite.tipo_est and tramite.uso and tramite.legalizacion) and tramite.tipo_est.strip()!= '' and tramite.uso.strip()!= ''
        context['Posgrado_Internacional'] = tramite.tipo_posi and tramite.tipo_posi.strip()!= ''
        context['Posgrado_Internacional_Legalizacion'] = (tramite.tipo_est and tramite.uso_i and tramite.legalizacion) and tramite.tipo_est.strip()!= '' and tramite.uso_i.strip()!= ''
        return context
    
@login_required
@administracion_required
def Informacion_Usuario(request,id):
    usuario = Usuario.objects.get(id=id)
    if request.POST:
        usuario.first_name = request.POST['first_name']
        usuario.last_name = request.POST['last_name']
        usuario.carnet = request.POST['carnet']
        usuario.email = request.POST['email']
        usuario.telefono = request.POST['telefono']
        usuario.save()
        return redirect("Usuarios")
    form = InformacionPersonalForm(instance=usuario)
    return render(request,"General/informacion_usuario.html",{"form":form})




