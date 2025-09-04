from django.core.management.base import BaseCommand
from core.models import FAQ, SiteConfiguration, Banner


class Command(BaseCommand):
    help = 'Populate the database with sample core data'

    def handle(self, *args, **options):
        self.stdout.write('Creating FAQs...')
        
        # Create FAQs
        faqs_data = [
            {
                'question': 'How long does it take to process my order?',
                'answer': 'Most orders are processed within 24-48 hours. Express services are available for same-day processing.',
                'category': 'General',
                'order': 1
            },
            {
                'question': 'What payment methods do you accept?',
                'answer': 'We accept cash on delivery, online payments via Razorpay, and digital wallets.',
                'category': 'Payment',
                'order': 2
            },
            {
                'question': 'Do you provide pickup and delivery services?',
                'answer': 'Yes, we provide free pickup and delivery services within our service areas.',
                'category': 'Delivery',
                'order': 3
            },
            {
                'question': 'What if I\'m not satisfied with the service?',
                'answer': 'We offer a 100% satisfaction guarantee. If you\'re not happy, we\'ll redo the service for free.',
                'category': 'Quality',
                'order': 4
            },
            {
                'question': 'How do I track my order?',
                'answer': 'You can track your order through our website or mobile app using your order number.',
                'category': 'Tracking',
                'order': 5
            },
            {
                'question': 'What are your operating hours?',
                'answer': 'We operate 7 days a week from 8 AM to 8 PM. Emergency services are available 24/7.',
                'category': 'General',
                'order': 6
            }
        ]
        
        for faq_data in faqs_data:
            faq, created = FAQ.objects.get_or_create(
                question=faq_data['question'],
                defaults=faq_data
            )
            if created:
                self.stdout.write(f'Created FAQ: {faq.question}')
        
        self.stdout.write('Creating site configurations...')
        
        # Create site configurations
        configs_data = [
            {
                'key': 'site_name',
                'value': 'Smart Laundry',
                'description': 'Name of the website'
            },
            {
                'key': 'contact_email',
                'value': 'info@smartlaundry.com',
                'description': 'Contact email address'
            },
            {
                'key': 'contact_phone',
                'value': '+91 9876543210',
                'description': 'Contact phone number'
            },
            {
                'key': 'delivery_charge',
                'value': '50',
                'description': 'Standard delivery charge in rupees'
            },
            {
                'key': 'tax_rate',
                'value': '18',
                'description': 'GST rate in percentage'
            },
            {
                'key': 'min_order_amount',
                'value': '100',
                'description': 'Minimum order amount in rupees'
            }
        ]
        
        for config_data in configs_data:
            config, created = SiteConfiguration.objects.get_or_create(
                key=config_data['key'],
                defaults=config_data
            )
            if created:
                self.stdout.write(f'Created config: {config.key}')
        
        self.stdout.write('Creating banners...')
        
        # Create banners
        banners_data = [
            {
                'title': 'Professional Laundry Services',
                'subtitle': 'Get your clothes cleaned, pressed, and delivered to your doorstep',
                'link_url': '/services',
                'order': 1
            },
            {
                'title': 'Same Day Service Available',
                'subtitle': 'Express cleaning and pressing services for urgent needs',
                'link_url': '/services',
                'order': 2
            },
            {
                'title': 'Free Pickup & Delivery',
                'subtitle': 'Convenient pickup and delivery services at no extra cost',
                'link_url': '/contact',
                'order': 3
            }
        ]
        
        for banner_data in banners_data:
            banner, created = Banner.objects.get_or_create(
                title=banner_data['title'],
                defaults=banner_data
            )
            if created:
                self.stdout.write(f'Created banner: {banner.title}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated core data!')
        )