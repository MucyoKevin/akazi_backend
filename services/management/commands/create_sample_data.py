from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from services.models import ServiceCategory, Service
from accounts.models import ServiceProvider, CustomerProfile
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample data for the Akazi application'
    
    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create service categories
        categories_data = [
            {
                'name': 'House Cleaning',
                'description': 'Professional cleaning services for homes and offices'
            },
            {
                'name': 'Plumbing',
                'description': 'Expert plumbing repairs and installations'
            },
            {
                'name': 'Electrical',
                'description': 'Licensed electrical work and repairs'
            },
            {
                'name': 'Gardening',
                'description': 'Garden maintenance and landscaping services'
            },
            {
                'name': 'Painting',
                'description': 'Interior and exterior painting services'
            },
            {
                'name': 'Carpentry',
                'description': 'Custom woodwork and furniture repair'
            },
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = ServiceCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create services
        services_data = [
            {'name': 'Deep House Cleaning', 'category': 'House Cleaning', 'base_price': 15000},
            {'name': 'Regular House Cleaning', 'category': 'House Cleaning', 'base_price': 8000},
            {'name': 'Office Cleaning', 'category': 'House Cleaning', 'base_price': 12000},
            {'name': 'Pipe Repair', 'category': 'Plumbing', 'base_price': 10000},
            {'name': 'Drain Cleaning', 'category': 'Plumbing', 'base_price': 7500},
            {'name': 'Toilet Installation', 'category': 'Plumbing', 'base_price': 25000},
            {'name': 'Electrical Wiring', 'category': 'Electrical', 'base_price': 20000},
            {'name': 'Light Installation', 'category': 'Electrical', 'base_price': 5000},
            {'name': 'Garden Maintenance', 'category': 'Gardening', 'base_price': 12000},
            {'name': 'Lawn Mowing', 'category': 'Gardening', 'base_price': 6000},
            {'name': 'Interior Painting', 'category': 'Painting', 'base_price': 18000},
            {'name': 'Exterior Painting', 'category': 'Painting', 'base_price': 22000},
            {'name': 'Furniture Repair', 'category': 'Carpentry', 'base_price': 15000},
            {'name': 'Custom Shelving', 'category': 'Carpentry', 'base_price': 30000},
        ]
        
        for service_data in services_data:
            try:
                category = ServiceCategory.objects.get(name=service_data['category'])
                service, created = Service.objects.get_or_create(
                    name=service_data['name'],
                    category=category,
                    defaults={
                        'description': f'Professional {service_data["name"].lower()} service',
                        'base_price': Decimal(str(service_data['base_price']))
                    }
                )
                if created:
                    self.stdout.write(f'Created service: {service.name}')
            except ServiceCategory.DoesNotExist:
                self.stdout.write(f'Category "{service_data["category"]}" not found for service {service_data["name"]}')
        
        # Create sample users and providers
        sample_providers = [
            {
                'username': 'john_cleaner',
                'phone_number': '+250785141480',
                'user_type': 'provider',
                'location': 'Kigali',
                'bio': 'Professional cleaner with 5 years experience',
                'hourly_rate': 2500
            },
            {
                'username': 'marie_plumber',
                'phone_number': '+250788123456',
                'user_type': 'provider',
                'location': 'Gasabo',
                'bio': 'Licensed plumber specializing in residential repairs',
                'hourly_rate': 3000
            },
            {
                'username': 'paul_electrician',
                'phone_number': '+250789654321',
                'user_type': 'provider',
                'location': 'Nyarugenge',
                'bio': 'Certified electrician with 8 years experience',
                'hourly_rate': 3500
            }
        ]
        
        for provider_data in sample_providers:
            if not User.objects.filter(username=provider_data['username']).exists():
                user = User.objects.create_user(
                    username=provider_data['username'],
                    phone_number=provider_data['phone_number'],
                    user_type=provider_data['user_type'],
                    location=provider_data['location'],
                    is_phone_verified=True
                )
                user.set_password('testpass123')
                user.save()
                
                provider_profile = ServiceProvider.objects.create(
                    user=user,
                    bio=provider_data['bio'],
                    hourly_rate=Decimal(str(provider_data['hourly_rate'])),
                    is_verified=True,
                    rating=Decimal('4.5')
                )
                
                self.stdout.write(f'Created provider: {user.username}')
        
        # Create sample customers
        sample_customers = [
            {
                'username': 'alice_customer',
                'phone_number': '+250781234567',
                'user_type': 'customer',
                'location': 'Kicukiro'
            },
            {
                'username': 'bob_customer',
                'phone_number': '+250787654321',
                'user_type': 'customer',
                'location': 'Remera'
            }
        ]
        
        for customer_data in sample_customers:
            if not User.objects.filter(username=customer_data['username']).exists():
                user = User.objects.create_user(
                    username=customer_data['username'],
                    phone_number=customer_data['phone_number'],
                    user_type=customer_data['user_type'],
                    location=customer_data['location'],
                    is_phone_verified=True
                )
                user.set_password('testpass123')
                user.save()
                
                CustomerProfile.objects.create(user=user)
                
                self.stdout.write(f'Created customer: {user.username}')
        
        self.stdout.write(
            self.style.SUCCESS('Sample data created successfully!')
        )