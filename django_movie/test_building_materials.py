#!/usr/bin/env python
"""
Test script for building materials store functionality
Run this script to verify that all components work correctly after migration
"""

import os
import sys
import django
from django.test import TestCase
from django.core.management import call_command
from django.db import connection
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_movie.settings')
django.setup()

from movies.models import (
    Products, Category, MaterialType, MaterialGrade, 
    TechnicalStandard, ApplicationArea, EquipmentType, 
    UnitOfMeasure, Manufacturer, ProductVariant
)

class BuildingMaterialsTestSuite:
    """Comprehensive test suite for building materials store"""
    
    def __init__(self):
        self.passed_tests = 0
        self.failed_tests = 0
        self.test_results = []
    
    def run_test(self, test_name, test_func):
        """Run a single test and record results"""
        try:
            print(f"Running {test_name}...", end=" ")
            test_func()
            print("✅ PASSED")
            self.passed_tests += 1
            self.test_results.append((test_name, "PASSED", None))
        except Exception as e:
            print(f"❌ FAILED: {str(e)}")
            self.failed_tests += 1
            self.test_results.append((test_name, "FAILED", str(e)))
    
    def test_model_creation(self):
        """Test that all new models can be created"""
        # Test MaterialType
        material_type = MaterialType.objects.create(
            title_ru="Тестовый материал",
            title_uz="Test material",
            title_eng="Test Material"
        )
        assert material_type.id is not None
        
        # Test Manufacturer
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country_ru="Россия",
            website="https://test.com"
        )
        assert manufacturer.id is not None
        
        # Test UnitOfMeasure
        unit = UnitOfMeasure.objects.create(
            name_ru="Тестовая единица",
            name_uz="Test birlik",
            name_eng="Test Unit",
            symbol="тест"
        )
        assert unit.id is not None
        
        print("All new models created successfully")
    
    def test_product_creation(self):
        """Test building materials product creation"""
        # Create required references
        category = Category.objects.create(
            number=999,
            title_ru="Тестовая категория",
            status=True
        )
        
        material_type = MaterialType.objects.create(
            title_ru="Тестовый материал",
            title_uz="Test material",
            title_eng="Test Material"
        )
        
        unit = UnitOfMeasure.objects.create(
            name_ru="Штука",
            name_uz="Dona",
            name_eng="Piece",
            symbol="шт"
        )
        
        # Create product with building materials attributes
        product = Products.objects.create(
            title_ru="Тестовый строительный материал",
            title_uz="Test qurilish materiali",
            title_eng="Test Building Material",
            description_ru="Описание тестового материала",
            specifications_ru="Технические характеристики",
            installation_guide_ru="Руководство по установке",
            length=1000.00,
            width=500.00,
            height=100.00,
            weight=25.500,
            price=15000.00,
            cost_price=10000.00,
            stock=100,
            min_stock_level=10,
            product_type='MATERIAL',
            unit_type='ШТ',
            material_composition="Сталь, покрытие цинк",
            certificate_number="CERT-2024-001",
            fire_resistance_class="A1",
            environmental_class="E1",
            categoty_id=category,
            material_type_id=material_type,
            unit_of_measure=unit,
            is_available=True,
            is_professional=False,
            requires_delivery=True
        )
        
        assert product.id is not None
        assert product.is_in_stock == True
        assert product.is_low_stock == False
        assert product.total_dimensions == 0.05  # 1m * 0.5m * 0.1m
        assert product.profit_margin == 33.33333333333333  # (15000-10000)/15000*100
        
        print("Building materials product created with all attributes")
    
    def test_product_variants(self):
        """Test product variants functionality"""
        # Create base product
        category = Category.objects.create(
            number=998,
            title_ru="Тестовая категория 2",
            status=True
        )
        
        product = Products.objects.create(
            title_ru="Базовый продукт",
            price=10000.00,
            stock=50,
            categoty_id=category,
            product_type='MATERIAL'
        )
        
        # Create variant
        variant = ProductVariant.objects.create(
            product=product,
            variant_name_ru="Вариант 1000x500",
            length=1000.00,
            width=500.00,
            height=50.00,
            color="Белый",
            price=12000.00,
            stock=25,
            sku="VAR-001",
            is_available=True
        )
        
        assert variant.id is not None
        assert variant.is_in_stock == True
        assert "Вариант 1000x500" in str(variant)
        
        print("Product variants working correctly")
    
    def test_database_indexes(self):
        """Test that database indexes are created properly"""
        with connection.cursor() as cursor:
            # Check if indexes exist on Products table
            cursor.execute("""
                SELECT COUNT(*) FROM information_schema.statistics 
                WHERE table_name = 'movies_products' 
                AND table_schema = DATABASE()
            """)
            index_count = cursor.fetchone()[0]
            
            assert index_count > 5, f"Expected more than 5 indexes, found {index_count}"
            
        print("Database indexes are properly created")
    
    def test_api_compatibility(self):
        """Test that existing API structure still works"""
        from movies.views import ProductsDetailView, CategorytDetailView
        
        # Test that views can be instantiated
        products_view = ProductsDetailView()
        category_view = CategorytDetailView()
        
        assert hasattr(products_view, 'get_queryset')
        assert hasattr(category_view, 'get_queryset')
        
        print("API views are compatible")
    
    def test_admin_configuration(self):
        """Test admin interface configuration"""
        from django.contrib import admin
        from movies.models import Products, MaterialType, Manufacturer
        
        # Check if models are registered in admin
        assert Products in admin.site._registry
        
        print("Admin interface properly configured")
    
    def test_multilingual_support(self):
        """Test multilingual field support"""
        material_type = MaterialType.objects.create(
            title_uz="O'zbek nomi",
            title_ru="Русское название",
            title_eng="English Name"
        )
        
        assert material_type.title_uz == "O'zbek nomi"
        assert material_type.title_ru == "Русское название"
        assert material_type.title_eng == "English Name"
        assert str(material_type) == "Русское название"
        
        print("Multilingual support working correctly")
    
    def test_fixtures_loading(self):
        """Test that fixtures can be loaded"""
        try:
            call_command('loaddata', 'fixtures/building_materials_categories.json', verbosity=0)
            call_command('loaddata', 'fixtures/material_types.json', verbosity=0)
            call_command('loaddata', 'fixtures/equipment_types.json', verbosity=0)
            
            # Verify data was loaded
            assert Category.objects.filter(title_ru="Строительные материалы").exists()
            assert MaterialType.objects.filter(title_ru="Металл").exists()
            assert EquipmentType.objects.filter(title_ru="Сверлильные инструменты").exists()
            
            print("Fixtures loaded successfully")
        except Exception as e:
            raise Exception(f"Fixture loading failed: {e}")
    
    def test_search_functionality(self):
        """Test search functionality with building materials"""
        # Create test products
        category = Category.objects.create(
            number=997,
            title_ru="Поиск категория",
            status=True
        )
        
        Products.objects.create(
            title_ru="Дрель электрическая",
            description_ru="Профессиональная дрель",
            product_type='TOOL',
            price=5000.00,
            stock=10,
            categoty_id=category,
            is_available=True
        )
        
        Products.objects.create(
            title_ru="Цемент портландский",
            description_ru="Высококачественный цемент",
            product_type='MATERIAL',
            price=500.00,
            stock=100,
            categoty_id=category,
            is_available=True
        )
        
        # Test search
        tools = Products.objects.filter(product_type='TOOL')
        materials = Products.objects.filter(product_type='MATERIAL')
        
        assert tools.count() >= 1
        assert materials.count() >= 1
        
        print("Search functionality working with building materials")
    
    def run_all_tests(self):
        """Run all tests and provide summary"""
        print("🏗️  Building Materials Store Test Suite")
        print("=" * 50)
        
        # List of all tests
        tests = [
            ("Model Creation", self.test_model_creation),
            ("Product Creation", self.test_product_creation),
            ("Product Variants", self.test_product_variants),
            ("Database Indexes", self.test_database_indexes),
            ("API Compatibility", self.test_api_compatibility),
            ("Admin Configuration", self.test_admin_configuration),
            ("Multilingual Support", self.test_multilingual_support),
            ("Fixtures Loading", self.test_fixtures_loading),
            ("Search Functionality", self.test_search_functionality),
        ]
        
        # Run all tests
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 Test Summary:")
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"📈 Success Rate: {(self.passed_tests/(self.passed_tests+self.failed_tests)*100):.1f}%")
        
        if self.failed_tests > 0:
            print("\n❌ Failed Tests:")
            for test_name, status, error in self.test_results:
                if status == "FAILED":
                    print(f"  - {test_name}: {error}")
        
        print("\n🎉 Building Materials Store is ready!" if self.failed_tests == 0 else "\n⚠️  Some tests failed - please review")
        
        return self.failed_tests == 0

if __name__ == "__main__":
    test_suite = BuildingMaterialsTestSuite()
    success = test_suite.run_all_tests()
    sys.exit(0 if success else 1)