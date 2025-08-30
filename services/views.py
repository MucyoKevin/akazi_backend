from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import ServiceCategory, Service
from .serializers import ServiceCategorySerializer, ServiceSerializer

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
