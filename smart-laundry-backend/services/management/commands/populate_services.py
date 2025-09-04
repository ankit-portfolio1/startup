from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from services.models import ServiceCategory, Service, ServiceOption


class Command(BaseCommand):
    help = 'Populate the database with sample services data'

    def handle(self, *args, **options):
        self.stdout.write('Creating service categories...')
        
        # Create service categories
        categories_data = [
            {
                'name': 'Steam Pressing',
                'emoji': '🧺',
                'description': 'Professional steam pressing services for wrinkle-free clothes'
            },
            {
                'name': 'Dry Cleaning',
                'emoji': '👔',
                'description': 'Expert dry cleaning for delicate and formal wear'
            },
            {
                'name': 'Wash & Fold',
                'emoji': '🛏️',
                'description': 'Convenient wash and fold services for everyday clothes'
            },
            {
                'name': 'Ironing',
                'emoji': '👕',
                'description': 'Professional ironing services for crisp, clean clothes'
            }
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = ServiceCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        self.stdout.write('Creating services...')
        
        # Create services
        services_data = [
            {
                'category': 'Steam Pressing',
                'name': 'Steam Pressing',
                'emoji': '🧺',
                'description': 'Professional steam pressing for wrinkle-free, confidence-ready clothes',
                'price': 15.00,
                'estimated_time': timedelta(hours=2),
                'options': [
                    {'name': 'Shirt', 'emoji': '👔', 'price': 15},
                    {'name': 'T-Shirt', 'emoji': '👕', 'price': 12},
                    {'name': 'Kurta', 'emoji': '🧕', 'price': 18},
                    {'name': 'Jeans', 'emoji': '👖', 'price': 20},
                ]
            },
            {
                'category': 'Dry Cleaning',
                'name': 'Dry Cleaning',
                'emoji': '👔',
                'description': 'Expert dry cleaning for delicate and formal wear',
                'price': 120.00,
                'estimated_time': timedelta(hours=24),
                'options': [
                    {'name': 'Saree', 'emoji': '🧣', 'price': 120},
                    {'name': 'Suit / Blazer', 'emoji': '🤵', 'price': 150},
                    {'name': 'Dress / Gown', 'emoji': '👗', 'price': 140},
                    {'name': 'Sherwani', 'emoji': '👘', 'price': 160},
                ]
            },
            {
                'category': 'Wash & Fold',
                'name': 'Wash & Fold',
                'emoji': '🛏️',
                'description': 'Convenient wash and fold services for everyday clothes',
                'price': 8.00,
                'estimated_time': timedelta(hours=6),
                'options': [
                    {'name': 'T-Shirt', 'emoji': '👕', 'price': 8},
                    {'name': 'Shirt', 'emoji': '👔', 'price': 10},
                    {'name': 'Jeans', 'emoji': '👖', 'price': 12},
                    {'name': 'Trousers', 'emoji': '👖', 'price': 10},
                ]
            },
            {
                'category': 'Ironing',
                'name': 'Ironing',
                'emoji': '👕',
                'description': 'Professional ironing services for crisp, clean clothes',
                'price': 5.00,
                'estimated_time': timedelta(hours=1),
                'options': [
                    {'name': 'Shirt', 'emoji': '👔', 'price': 5},
                    {'name': 'T-Shirt', 'emoji': '👕', 'price': 4},
                    {'name': 'Kurta', 'emoji': '🧕', 'price': 6},
                    {'name': 'Trousers', 'emoji': '👖', 'price': 5},
                ]
            }
        ]
        
        for service_data in services_data:
            category = categories[service_data['category']]
            options_data = service_data.pop('options')
            service_data['category'] = category
            
            service, created = Service.objects.get_or_create(
                category=category,
                name=service_data['name'],
                defaults=service_data
            )
            
            if created:
                self.stdout.write(f'Created service: {service.name}')
                
                # Create service options
                for option_data in options_data:
                    ServiceOption.objects.create(
                        service=service,
                        **option_data
                    )
                    self.stdout.write(f'  Created option: {option_data["name"]}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated services data!')
        )