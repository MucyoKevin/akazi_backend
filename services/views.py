from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import ServiceCategory, Service, ServicePackage
from .serializers import ServiceCategorySerializer, ServiceSerializer, ServiceDetailSerializer, ServicePackageSerializer

class ServiceCategoryListView(generics.ListAPIView):
    queryset = ServiceCategory.objects.filter(is_active=True)
    serializer_class = ServiceCategorySerializer
    permission_classes = [AllowAny]

class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

class ServiceDetailView(generics.RetrieveAPIView):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceDetailSerializer
    permission_classes = [AllowAny]

@api_view(['GET'])
@permission_classes([AllowAny])
def service_packages(request, service_id):
    """Get packages for a specific service"""
    try:
        service = Service.objects.get(id=service_id, is_active=True)
        packages = ServicePackage.objects.filter(service=service, is_active=True).order_by('price')
        serializer = ServicePackageSerializer(packages, many=True)
        return Response(serializer.data)
    except Service.DoesNotExist:
        return Response({'error': 'Service not found'}, status=404)

@api_view(['GET'])
@permission_classes([AllowAny])
def service_providers(request, service_id):
    """Get providers for a specific service"""
    try:
        from accounts.models import ServiceProvider
        from accounts.serializers import ServiceProviderSerializer
        
        service = Service.objects.get(id=service_id, is_active=True)
        providers = ServiceProvider.objects.filter(
            services_offered=service,
            is_verified=True
        ).order_by('-rating', '-total_reviews')
        
        # Filter by availability if requested
        availability = request.query_params.get('availability')
        if availability:
            providers = providers.filter(availability_status=availability)
        
        serializer = ServiceProviderSerializer(providers, many=True)
        return Response(serializer.data)
    except Service.DoesNotExist:
        return Response({'error': 'Service not found'}, status=404)

@api_view(['GET'])
@permission_classes([AllowAny])
def featured_providers(request):
    from accounts.models import ServiceProvider
    from accounts.serializers import ServiceProviderSerializer
    
    providers = ServiceProvider.objects.filter(
        is_verified=True,
        is_available=True
    ).order_by('-rating')[:10]
    
    serializer = ServiceProviderSerializer(providers, many=True)
    return Response(serializer.data)
