from rest_framework import serializers
from .models import ServiceCategory, Service, Review, ServicePackage

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'icon', 'description']

class ServicePackageSerializer(serializers.ModelSerializer):
    duration_display = serializers.ReadOnlyField()
    
    class Meta:
        model = ServicePackage
        fields = ['id', 'name', 'description', 'duration_min', 'duration_max', 
                 'duration_display', 'price', 'is_popular']

class ServiceSerializer(serializers.ModelSerializer):
    category = ServiceCategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    packages = ServicePackageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'base_price', 'category', 'category_id', 'packages']

class ServiceDetailSerializer(serializers.ModelSerializer):
    category = ServiceCategorySerializer(read_only=True)
    packages = ServicePackageSerializer(many=True, read_only=True)
    provider_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    price_range = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'base_price', 'category', 'packages',
                 'provider_count', 'average_rating', 'price_range']
    
    def get_provider_count(self, obj):
        from accounts.models import ServiceProvider
        return ServiceProvider.objects.filter(services_offered=obj, is_verified=True).count()
    
    def get_average_rating(self, obj):
        from accounts.models import ServiceProvider
        providers = ServiceProvider.objects.filter(services_offered=obj, is_verified=True)
        if providers.exists():
            total_rating = sum(p.rating for p in providers)
            return round(total_rating / providers.count(), 1)
        return 0.0
    
    def get_price_range(self, obj):
        packages = obj.packages.filter(is_active=True)
        if packages.exists():
            min_price = min(p.price for p in packages)
            max_price = max(p.price for p in packages)
            return f"{int(min_price):,} - {int(max_price):,} RWF"
        return f"{int(obj.base_price):,} RWF"

class ReviewSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.username', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'rating', 'comment', 'customer_name', 'created_at']
