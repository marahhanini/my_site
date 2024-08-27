from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .models import PressureSensor, PressureReading
from .serializers import PressureSensorSerializer, PressureReadingSerializer
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Custom permission class
class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

# ViewSets for PressureSensor and PressureReading
class PressureSensorViewSet(viewsets.ModelViewSet):
    queryset = PressureSensor.objects.all()
    serializer_class = PressureSensorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class PressureReadingViewSet(viewsets.ModelViewSet):
    queryset = PressureReading.objects.all()
    serializer_class = PressureReadingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# Aggregate view for pressure readings
class AggregatePressureReadingsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        since = request.GET.get('since')
        until = request.GET.get('until')
        calculation = request.GET.get('calculation')
        
        # Add logic for aggregation here
        # e.g., filter PressureReading objects based on `since` and `until`,
        # and apply `calculation` logic (e.g., average, sum)
        
        return Response({'message': 'Aggregation logic not implemented yet'})

# Greeting view
@method_decorator(login_required(login_url='/admin/login/'), name='dispatch')
def greeting(request):
    return JsonResponse({'message': f'Hello {request.user.username}!'})
