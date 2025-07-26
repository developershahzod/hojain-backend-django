from django.core.management.base import BaseCommand
from django.db import transaction
from movies.models import (
    Products, Category, MaterialType, MaterialGrade, 
    TechnicalStandard, ApplicationArea, EquipmentType, 
    UnitOfMeasure, Manufacturer
)
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Transform existing cosmetics data to building materials structure'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be changed without making actual changes',
        )
        parser.add_argument(
            '--preserve-data',
            action='store_true',
            help='Preserve existing data where possible',
        )
    
    def handle(self, *args, **options):
        dry_run = options['dry_run']
        preserve_data = options['preserve_data']
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('DRY RUN MODE - No changes will be made')
            )
        
        try:
            with transaction.atomic():
                self.transform_categories()
                self.transform_products(preserve_data)
                self.create_default_references()
                
                if dry_run:
                    # Rollback the transaction in dry run mode
                    raise Exception("Dry run completed - rolling back changes")
                    
        except Exception as e:
            if "Dry run completed" in str(e):
                self.stdout.write(
                    self.style.SUCCESS('Dry run completed successfully')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'Error during transformation: {e}')
                )
                raise
        
        if not dry_run:
            self.stdout.write(
                self.style.SUCCESS('Successfully transformed to building materials store')
            )
    
    def transform_categories(self):
        """Transform existing categories to building materials context"""
        self.stdout.write('Transforming categories...')
        
        # Update main categories
        category_mappings = {
            'косметика': {
                'title_ru': 'Строительные материалы',
                'title_uz': 'Qurilish materiallari',
                'title_eng': 'Construction Materials',
                'icon': 'fas fa-hammer'
            },
            'красота': {
                'title_ru': 'Инструменты и оборудование',
                'title_uz': 'Asboblar va uskunalar',
                'title_eng': 'Tools and Equipment',
                'icon': 'fas fa-tools'
            },
            'уход': {
                'title_ru': 'Крепежные изделия',
                'title_uz': 'Mahkamlagichlar',
                'title_eng': 'Hardware & Fasteners',
                'icon': 'fas fa-screwdriver'
            }
        }
        
        for old_keyword, new_data in category_mappings.items():
            categories = Category.objects.filter(
                title_ru__icontains=old_keyword
            )
            
            for category in categories:
                self.stdout.write(f'  Updating category: {category.title_ru}')
                for field, value in new_data.items():
                    setattr(category, field, value)
                category.save()
    
    def transform_products(self, preserve_data):
        """Transform existing products to building materials"""
        self.stdout.write('Transforming products...')
        
        # Get or create default references
        default_material_type, _ = MaterialType.objects.get_or_create(
            title_ru='Общие материалы',
            defaults={
                'title_uz': 'Umumiy materiallar',
                'title_eng': 'General Materials'
            }
        )
        
        default_unit, _ = UnitOfMeasure.objects.get_or_create(
            symbol='шт',
            defaults={
                'name_ru': 'Штука',
                'name_uz': 'Dona',
                'name_eng': 'Piece'
            }
        )
        
        products_updated = 0
        
        for product in Products.objects.all():
            self.stdout.write(f'  Processing product: {product.title_ru}')
            
            # Determine product type based on existing data
            title_lower = (product.title_ru or '').lower()
            
            if any(keyword in title_lower for keyword in ['инструмент', 'дрель', 'пила']):
                product.product_type = 'TOOL'
            elif any(keyword in title_lower for keyword in ['оборудование', 'станок']):
                product.product_type = 'EQUIPMENT'
            elif any(keyword in title_lower for keyword in ['болт', 'винт', 'гайка']):
                product.product_type = 'FASTENER'
            elif any(keyword in title_lower for keyword in ['краска', 'клей', 'герметик']):
                product.product_type = 'CHEMICAL'
            else:
                product.product_type = 'MATERIAL'
            
            # Set default values for new fields
            if not hasattr(product, 'material_type_id') or not product.material_type_id:
                product.material_type_id = default_material_type
            
            if not hasattr(product, 'unit_of_measure') or not product.unit_of_measure:
                product.unit_of_measure = default_unit
            
            # Transform volume to unit measurements
            if hasattr(product, 'volume_type'):
                unit_mapping = {
                    'МЛ': 'Л',
                    'Г': 'КГ',
                    'ШТ': 'ШТ'
                }
                product.unit_type = unit_mapping.get(product.volume_type, 'ШТ')
            
            # Set building materials specific defaults
            product.is_available = True
            product.delivery_days = 3
            product.requires_delivery = True
            product.is_hazardous = False
            product.is_fragile = False
            
            # Transform cosmetic fields to building materials
            if preserve_data:
                # Move cosmetic descriptions to specifications
                if hasattr(product, 'naznachenie_ru') and product.naznachenie_ru:
                    product.specifications_ru = product.naznachenie_ru
                if hasattr(product, 'naznachenie_uz') and product.naznachenie_uz:
                    product.specifications_uz = product.naznachenie_uz
                if hasattr(product, 'naznachenie_eng') and product.naznachenie_eng:
                    product.specifications_eng = product.naznachenie_eng
                
                # Move application info to installation guide
                if hasattr(product, 'primeneniye_ru') and product.primeneniye_ru:
                    product.installation_guide_ru = product.primeneniye_ru
                if hasattr(product, 'primeneniye_uz') and product.primeneniye_uz:
                    product.installation_guide_uz = product.primeneniye_uz
                if hasattr(product, 'primeneniye_eng') and product.primeneniye_eng:
                    product.installation_guide_eng = product.primeneniye_eng
                
                # Move composition to material composition
                if hasattr(product, 'sostav') and product.sostav:
                    product.material_composition = product.sostav
            
            product.save()
            products_updated += 1
        
        self.stdout.write(f'  Updated {products_updated} products')
    
    def create_default_references(self):
        """Create default reference data if not exists"""
        self.stdout.write('Creating default reference data...')
        
        # Create default material types
        default_materials = [
            ('Металл', 'Metall', 'Metal'),
            ('Древесина', 'Yog\'och', 'Wood'),
            ('Бетон', 'Beton', 'Concrete'),
            ('Пластик', 'Plastik', 'Plastic'),
        ]
        
        for ru, uz, eng in default_materials:
            MaterialType.objects.get_or_create(
                title_ru=ru,
                defaults={'title_uz': uz, 'title_eng': eng}
            )
        
        # Create default equipment types
        default_equipment = [
            ('Электроинструменты', 'Elektr asboblari', 'Power Tools', True, False),
            ('Ручные инструменты', 'Qo\'l asboblari', 'Hand Tools', False, False),
            ('Измерительные инструменты', 'O\'lchash asboblari', 'Measuring Tools', False, False),
        ]
        
        for ru, uz, eng, is_power, requires_cert in default_equipment:
            EquipmentType.objects.get_or_create(
                title_ru=ru,
                defaults={
                    'title_uz': uz,
                    'title_eng': eng,
                    'is_power_tool': is_power,
                    'requires_certification': requires_cert
                }
            )
        
        # Create default application areas
        default_areas = [
            ('Жилищное строительство', 'Uy qurilishi', 'Residential Construction'),
            ('Коммерческое строительство', 'Tijorat qurilishi', 'Commercial Construction'),
            ('Промышленное строительство', 'Sanoat qurilishi', 'Industrial Construction'),
        ]
        
        for ru, uz, eng in default_areas:
            ApplicationArea.objects.get_or_create(
                title_ru=ru,
                defaults={'title_uz': uz, 'title_eng': eng}
            )
        
        self.stdout.write('  Default reference data created')