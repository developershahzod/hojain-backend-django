from django.core.management.base import BaseCommand
from django.db import connection
from django.core.cache import cache
from movies.models import Products, Orders, Review, Clients


class Command(BaseCommand):
    help = 'Optimize database performance and clear cache'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear-cache',
            action='store_true',
            help='Clear all cache entries',
        )
        parser.add_argument(
            '--analyze-tables',
            action='store_true',
            help='Analyze database tables for optimization',
        )

    def handle(self, *args, **options):
        if options['clear_cache']:
            self.clear_cache()
        
        if options['analyze_tables']:
            self.analyze_tables()
        
        self.cleanup_data()
        self.stdout.write(
            self.style.SUCCESS('Database optimization completed successfully')
        )

    def clear_cache(self):
        """Clear all cache entries"""
        cache.clear()
        self.stdout.write(
            self.style.SUCCESS('Cache cleared successfully')
        )

    def analyze_tables(self):
        """Analyze database tables"""
        with connection.cursor() as cursor:
            tables = ['movies_products', 'movies_orders', 'movies_review', 'movies_clients']
            
            for table in tables:
                try:
                    cursor.execute(f"ANALYZE TABLE {table}")
                    self.stdout.write(f"Analyzed table: {table}")
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error analyzing {table}: {e}")
                    )

    def cleanup_data(self):
        """Clean up old or invalid data"""
        # Remove products with zero stock that are older than 30 days
        old_products = Products.objects.filter(
            stock=0,
            created_at__lt=timezone.now() - timedelta(days=30)
        )
        count = old_products.count()
        if count > 0:
            self.stdout.write(f"Found {count} old products with zero stock")
        
        # Remove old search stories (older than 90 days)
        from movies.models import SearchStory
        old_searches = SearchStory.objects.filter(
            created_at__lt=timezone.now() - timedelta(days=90)
        )
        deleted_count = old_searches.count()
        old_searches.delete()
        
        if deleted_count > 0:
            self.stdout.write(f"Deleted {deleted_count} old search records")