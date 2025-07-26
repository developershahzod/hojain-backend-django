# Migration Guide: From Cosmetics to Building Materials Store

## 🚀 Overview
This guide helps you migrate the existing cosmetics e-commerce system to a building materials and equipment store.

## ⚠️ Important Notes
- **Backup your database** before starting the migration
- This migration will modify existing data structures
- Some cosmetic-specific data will be lost during migration
- Plan for downtime during the migration process

## 📋 Pre-Migration Checklist

### 1. Database Backup
```bash
# MySQL backup
mysqldump -u username -p database_name > backup_before_migration.sql

# PostgreSQL backup
pg_dump -U username database_name > backup_before_migration.sql
```

### 2. Environment Setup
```bash
# Ensure you have the latest code
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install any new dependencies
pip install -r requirements.txt
```

## 🔄 Migration Steps

### Step 1: Create New Migrations
```bash
# Generate migrations for the new models
python manage.py makemigrations movies --name="add_building_materials_models"

# Review the generated migration file
# Edit if necessary to handle data preservation
```

### Step 2: Data Migration Strategy

#### Option A: Fresh Installation (Recommended for Development)
```bash
# Drop existing database (CAUTION: This deletes all data)
python manage.py flush --noinput

# Apply all migrations
python manage.py migrate

# Load initial data
python manage.py loaddata fixtures/building_materials_categories.json
python manage.py loaddata fixtures/material_types.json
python manage.py loaddata fixtures/equipment_types.json

# Create superuser
python manage.py createsuperuser
```

#### Option B: Preserve Existing Data (Production)
```bash
# Apply migrations (this will add new fields)
python manage.py migrate

# Run data transformation script
python manage.py shell < scripts/transform_cosmetics_to_building_materials.py

# Load additional reference data
python manage.py loaddata fixtures/material_types.json
python manage.py loaddata fixtures/equipment_types.json
```

### Step 3: Update Existing Products
Create a management command to transform existing products:

```python
# movies/management/commands/transform_products.py
from django.core.management.base import BaseCommand
from movies.models import Products, MaterialType, EquipmentType

class Command(BaseCommand):
    help = 'Transform cosmetic products to building materials'
    
    def handle(self, *args, **options):
        # Transform existing products
        for product in Products.objects.all():
            # Update product type based on category
            if 'beauty' in product.title_ru.lower():
                product.product_type = 'MATERIAL'
            elif 'tool' in product.title_ru.lower():
                product.product_type = 'TOOL'
            
            # Set default values for new fields
            product.is_available = True
            product.delivery_days = 3
            product.unit_type = 'ШТ'
            
            product.save()
            
        self.stdout.write(
            self.style.SUCCESS('Successfully transformed products')
        )
```

### Step 4: Update Categories
```bash
# Run category transformation
python manage.py shell -c "
from movies.models import Category
# Update existing categories to building materials context
Category.objects.filter(title_ru__icontains='косметика').update(
    title_ru='Строительные материалы',
    title_uz='Qurilish materiallari',
    title_eng='Construction Materials'
)
"
```

## 🗂️ Data Mapping

### Model Field Mapping
| Old Field (Cosmetics) | New Field (Building Materials) | Notes |
|----------------------|--------------------------------|-------|
| `for_whom_id` | `material_type_id` | Target demographic → Material type |
| `skin_type_id` | `material_grade_id` | Skin type → Material grade |
| `hair_type_id` | `technical_standard_id` | Hair type → Technical standard |
| `product_area_id` | `application_area_id` | Direct mapping |
| `volume_name_ru` | `unit_name_ru` | Volume → Unit of measure |
| `volume_type` | `unit_type` | Updated choices |
| `sostav` | `material_composition` | Composition field |
| `naznachenie_*` | `specifications_*` | Purpose → Specifications |
| `primeneniye_*` | `installation_guide_*` | Application → Installation |

### New Fields Added
- `length`, `width`, `height`, `weight` - Physical dimensions
- `cost_price` - Cost tracking
- `min_stock_level` - Inventory management
- `manufacturer` - Manufacturer relationship
- `product_type` - Product classification
- `is_professional` - Professional grade flag
- `requires_delivery` - Delivery requirements
- `is_hazardous` - Safety classification
- `certificate_number` - Certification tracking
- `fire_resistance_class` - Safety rating
- `environmental_class` - Environmental rating

## 🔧 Post-Migration Tasks

### 1. Update Admin Interface
The admin interface has been updated with building materials context:
- New icons for construction industry
- Updated verbose names
- New custom links for reports

### 2. API Endpoints
New endpoints have been added:
- `/api/v1/products_material_type/{id}/` - Products by material type
- `/api/v1/products_equipment_type/{id}/` - Products by equipment type
- `/api/v1/products_manufacturer/{id}/` - Products by manufacturer
- `/api/v1/professional_products/` - Professional-grade products
- `/api/v1/low_stock_products/` - Low inventory alerts

### 3. Update Frontend (if applicable)
- Update product display templates
- Modify search filters for building materials
- Update category navigation
- Add new product specification displays

### 4. Test the Migration
```bash
# Run tests to ensure everything works
python manage.py test

# Check admin interface
python manage.py runserver
# Visit http://localhost:8000/admin/

# Test API endpoints
curl http://localhost:8000/api/v1/products/
curl http://localhost:8000/api/v1/categories/
```

## 🚨 Troubleshooting

### Common Issues

#### Migration Errors
```bash
# If migration fails, you can:
# 1. Check the migration file for issues
# 2. Run migrations one by one
python manage.py migrate movies 0001 --fake
python manage.py migrate movies 0002

# 3. Reset migrations (CAUTION: Development only)
python manage.py migrate movies zero
python manage.py migrate movies
```

#### Data Integrity Issues
```bash
# Check for orphaned records
python manage.py shell -c "
from movies.models import Products
print('Products without categories:', Products.objects.filter(categoty_id__isnull=True).count())
print('Products without brands:', Products.objects.filter(brand__isnull=True).count())
"
```

#### Performance Issues
```bash
# Rebuild database indexes
python manage.py dbshell
# Then run: ANALYZE TABLE movies_products;
```

## 📊 Validation Checklist

After migration, verify:
- [ ] All products have appropriate categories
- [ ] New building materials fields are populated
- [ ] API endpoints return correct data
- [ ] Admin interface displays properly
- [ ] Search functionality works with new fields
- [ ] Inventory tracking functions correctly
- [ ] Order processing works with new product types

## 🔄 Rollback Plan

If you need to rollback:

### 1. Database Rollback
```bash
# Restore from backup
mysql -u username -p database_name < backup_before_migration.sql
```

### 2. Code Rollback
```bash
# Revert to previous commit
git log --oneline  # Find the commit before migration
git checkout <previous-commit-hash>
```

### 3. Dependencies Rollback
```bash
# If requirements changed, restore previous version
git checkout HEAD~1 requirements.txt
pip install -r requirements.txt
```

## 📞 Support

If you encounter issues during migration:
1. Check the logs in `logs/django.log`
2. Review the migration files in `movies/migrations/`
3. Test with a small dataset first
4. Contact the development team for assistance

---

**Remember**: Always test the migration process in a development environment before applying to production!