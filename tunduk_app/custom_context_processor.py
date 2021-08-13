from .models import Service, Request_type

def service_type(request):
    service_types = Service.objects.all()
    data = {'service_types': service_types}
    return data
