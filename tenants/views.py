from django.http import HttpResponse

def tenant_view(request):
    return HttpResponse("This is a tenant-specific view")
