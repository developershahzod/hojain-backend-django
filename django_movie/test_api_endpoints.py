#!/usr/bin/env python
"""
Comprehensive API testing script for Building Materials Store
Tests all CRUD operations and endpoints
"""

import os
import sys
import django
import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_movie.settings')
django.setup()

from movies.models import (
    Products, Category, MaterialType, MaterialGrade, 
    TechnicalStandard, ApplicationArea, EquipmentType, 
    UnitOfMeasure, Manufacturer, ProductVariant, Brand
)

class BuildingMaterialsAPITestSuite(APITestCase):
    """Comprehensive API test suite for building materials store"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create test data
        self.category = Category.objects.create(
            number=1,
            title_ru="Тестовая категория",
            title_uz="Test kategoriya",
            title_eng="Test Category",
            status=True
        )
        
        self.material_type = MaterialType.objects.create(
            title_ru="Тестовый материал",
            title_uz="Test material",
            title_eng="Test Material"
        )
        
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country_ru="Россия",
            country_uz="Rossiya",
            country_eng="Russia"
        )
        
        self.unit = UnitOfMeasure.objects.create(
            name_ru="Штука",
            name_uz="Dona",
            name_eng="Piece",
            symbol="шт"
        )
        
        self.brand = Brand.objects.create(
            name="Test Brand"
        )
    
    def test_material_types_crud(self):
        """Test MaterialType CRUD operations"""
        print("Testing MaterialType CRUD...")
        
        # CREATE
        data = {
            "title_ru": "Новый материал",
            "title_uz": "Yangi material",
            "title_eng": "New Material"
        }
        response = self.client.post('/api/v1/material-types/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        material_id = response.data['id']
        
        # READ (List)
        response = self.client.get('/api/v1/material-types/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        
        # READ (Detail)
        response = self.client.get(f'/api/v1/material-types/{material_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title_ru'], "Новый материал")
        
        # UPDATE
        update_data = {"title_ru": "Обновленный материал"}
        response = self.client.patch(f'/api/v1/material-types/{material_id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title_ru'], "Обновленный материал")
        
        # DELETE
        response = self.client.delete(f'/api/v1/material-types/{material_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        print("✅ MaterialType CRUD tests passed")
    
    def test_manufacturers_crud(self):
        """Test Manufacturer CRUD operations"""
        print("Testing Manufacturer CRUD...")
        
        # CREATE
        data = {
            "name": "New Manufacturer",
            "country_ru": "Германия",
            "country_uz": "Germaniya",
            "country_eng": "Germany",
            "website": "https://example.com"
        }
        response = self.client.post('/api/v1/manufacturers/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        manufacturer_id = response.data['id']
        
        # READ (List)
        response = self.client.get('/api/v1/manufacturers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # READ (Detail)
        response = self.client.get(f'/api/v1/manufacturers/{manufacturer_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "New Manufacturer")
        
        # UPDATE
        update_data = {"name": "Updated Manufacturer"}
        response = self.client.patch(f'/api/v1/manufacturers/{manufacturer_id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # DELETE
        response = self.client.delete(f'/api/v1/manufacturers/{manufacturer_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        print("✅ Manufacturer CRUD tests passed")
    
    def test_building_materials_crud(self):
        """Test Building Materials Product CRUD operations"""
        print("Testing Building Materials CRUD...")
        
        # CREATE
        data = {
            "title_ru": "Тестовый продукт",
            "title_uz": "Test mahsulot",
            "title_eng": "Test Product",
            "description_ru": "Описание тестового продукта",
            "specifications_ru": "Технические характеристики",
            "price": "1000.00",
            "cost_price": "800.00",
            "stock": 50,
            "min_stock_level": 10,
            "product_type": "MATERIAL",
            "unit_type": "ШТ",
            "length": 100.00,
            "width": 50.00,
            "height": 25.00,
            "weight": 5.000,
            "material_composition": "Тестовый состав",
            "categoty_id": self.category.id,
            "material_type_id": self.material_type.id,
            "manufacturer": self.manufacturer.id,
            "unit_of_measure": self.unit.id,
            "brand": self.brand.id,
            "is_available": True,
            "is_professional": False
        }
        response = self.client.post('/api/v1/building-materials/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product_id = response.data['id']
        
        # READ (List)
        response = self.client.get('/api/v1/building-materials/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # READ (Detail)
        response = self.client.get(f'/api/v1/building-materials/{product_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title_ru'], "Тестовый продукт")
        
        # UPDATE
        update_data = {
            "title_ru": "Обновленный продукт",
            "price": "1200.00"
        }
        response = self.client.patch(f'/api/v1/building-materials/{product_id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # DELETE
        response = self.client.delete(f'/api/v1/building-materials/{product_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        print("✅ Building Materials CRUD tests passed")
    
    def test_product_variants_crud(self):
        """Test Product Variants CRUD operations"""
        print("Testing Product Variants CRUD...")
        
        # First create a product
        product = Products.objects.create(
            title_ru="Базовый продукт",
            price=1000.00,
            stock=50,
            categoty_id=self.category,
            product_type='MATERIAL'
        )
        
        # CREATE variant
        data = {
            "product": product.id,
            "variant_name_ru": "Вариант 1",
            "variant_name_uz": "Variant 1",
            "variant_name_eng": "Variant 1",
            "length": 200.00,
            "width": 100.00,
            "height": 50.00,
            "weight": 10.000,
            "color": "Красный",
            "price": "1100.00",
            "stock": 25,
            "sku": "VAR-001",
            "is_available": True
        }
        response = self.client.post('/api/v1/product-variants/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        variant_id = response.data['id']
        
        # READ (List)
        response = self.client.get('/api/v1/product-variants/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # READ (Detail)
        response = self.client.get(f'/api/v1/product-variants/{variant_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # READ (By Product)
        response = self.client.get(f'/api/v1/products/{product.id}/variants/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # UPDATE
        update_data = {"variant_name_ru": "Обновленный вариант"}
        response = self.client.patch(f'/api/v1/product-variants/{variant_id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # DELETE
        response = self.client.delete(f'/api/v1/product-variants/{variant_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        print("✅ Product Variants CRUD tests passed")
    
    def test_specialized_endpoints(self):
        """Test specialized product endpoints"""
        print("Testing specialized endpoints...")
        
        # Create test products
        professional_product = Products.objects.create(
            title_ru="Профессиональный инструмент",
            price=5000.00,
            stock=10,
            categoty_id=self.category,
            product_type='TOOL',
            is_professional=True,
            is_available=True
        )
        
        featured_product = Products.objects.create(
            title_ru="Рекомендуемый товар",
            price=2000.00,
            stock=20,
            categoty_id=self.category,
            product_type='MATERIAL',
            is_featured=True,
            is_available=True
        )
        
        low_stock_product = Products.objects.create(
            title_ru="Товар с низким остатком",
            price=1500.00,
            stock=2,
            min_stock_level=10,
            categoty_id=self.category,
            product_type='MATERIAL',
            is_available=True
        )
        
        # Test professional products
        response = self.client.get('/api/v1/products/professional/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        
        # Test featured products
        response = self.client.get('/api/v1/products/featured/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        
        # Test low stock products
        response = self.client.get('/api/v1/products/low-stock/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        
        print("✅ Specialized endpoints tests passed")
    
    def test_statistics_endpoints(self):
        """Test statistics and reports endpoints"""
        print("Testing statistics endpoints...")
        
        # Test product statistics
        response = self.client.get('/api/v1/stats/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_products', response.data)
        self.assertIn('in_stock_products', response.data)
        
        # Test inventory report
        response = self.client.get('/api/v1/reports/inventory/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        
        print("✅ Statistics endpoints tests passed")
    
    def test_bulk_operations(self):
        """Test bulk operations"""
        print("Testing bulk operations...")
        
        # Create test products
        product1 = Products.objects.create(
            title_ru="Продукт 1",
            price=1000.00,
            stock=50,
            categoty_id=self.category,
            product_type='MATERIAL'
        )
        
        product2 = Products.objects.create(
            title_ru="Продукт 2",
            price=2000.00,
            stock=30,
            categoty_id=self.category,
            product_type='TOOL'
        )
        
        # Test bulk stock update
        bulk_stock_data = {
            "updates": [
                {"product_id": product1.id, "stock": 75},
                {"product_id": product2.id, "stock": 45}
            ]
        }
        response = self.client.post('/api/v1/bulk/update-stock/', bulk_stock_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('updated_products', response.data)
        
        # Test bulk price update
        bulk_price_data = {
            "updates": [
                {"product_id": product1.id, "price": "1100.00"},
                {"product_id": product2.id, "price": "2200.00"}
            ]
        }
        response = self.client.post('/api/v1/bulk/update-prices/', bulk_price_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('updated_products', response.data)
        
        print("✅ Bulk operations tests passed")
    
    def test_search_and_filtering(self):
        """Test search and filtering functionality"""
        print("Testing search and filtering...")
        
        # Create searchable products
        Products.objects.create(
            title_ru="Дрель электрическая",
            price=3000.00,
            stock=15,
            categoty_id=self.category,
            product_type='TOOL',
            material_type_id=self.material_type,
            manufacturer=self.manufacturer,
            is_available=True
        )
        
        Products.objects.create(
            title_ru="Цемент портландский",
            price=800.00,
            stock=100,
            categoty_id=self.category,
            product_type='MATERIAL',
            material_type_id=self.material_type,
            manufacturer=self.manufacturer,
            is_available=True
        )
        
        # Test search
        response = self.client.get('/api/v1/building-materials/?search=дрель')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test filtering by material type
        response = self.client.get(f'/api/v1/products/material-type/{self.material_type.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test filtering by manufacturer
        response = self.client.get(f'/api/v1/products/manufacturer/{self.manufacturer.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        print("✅ Search and filtering tests passed")
    
    def test_validation(self):
        """Test API validation"""
        print("Testing validation...")
        
        # Test invalid price
        invalid_data = {
            "title_ru": "Невалидный продукт",
            "price": "-100.00",  # Invalid negative price
            "stock": 10,
            "product_type": "MATERIAL"
        }
        response = self.client.post('/api/v1/building-materials/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test invalid stock
        invalid_data = {
            "title_ru": "Невалидный продукт",
            "price": "100.00",
            "stock": -5,  # Invalid negative stock
            "product_type": "MATERIAL"
        }
        response = self.client.post('/api/v1/building-materials/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        print("✅ Validation tests passed")
    
    def run_all_tests(self):
        """Run all API tests"""
        print("🏗️  Building Materials API Test Suite")
        print("=" * 50)
        
        try:
            self.test_material_types_crud()
            self.test_manufacturers_crud()
            self.test_building_materials_crud()
            self.test_product_variants_crud()
            self.test_specialized_endpoints()
            self.test_statistics_endpoints()
            self.test_bulk_operations()
            self.test_search_and_filtering()
            self.test_validation()
            
            print("\n" + "=" * 50)
            print("🎉 All API tests passed successfully!")
            return True
            
        except Exception as e:
            print(f"\n❌ Test failed: {str(e)}")
            return False

def run_manual_api_tests():
    """Run manual API tests using Django test client"""
    print("🔧 Running Manual API Tests...")
    
    from django.test import Client
    client = Client()
    
    # Test basic endpoints
    endpoints_to_test = [
        '/api/v1/material-types/',
        '/api/v1/manufacturers/',
        '/api/v1/building-materials/',
        '/api/v1/stats/products/',
        '/api/v1/reports/inventory/',
    ]
    
    for endpoint in endpoints_to_test:
        try:
            response = client.get(endpoint)
            status_code = response.status_code
            print(f"  {endpoint}: {status_code} {'✅' if status_code == 200 else '❌'}")
        except Exception as e:
            print(f"  {endpoint}: Error - {str(e)} ❌")
    
    print("Manual API tests completed.")

if __name__ == "__main__":
    # Run automated tests
    test_suite = BuildingMaterialsAPITestSuite()
    test_suite.setUp()
    success = test_suite.run_all_tests()
    
    # Run manual tests
    run_manual_api_tests()
    
    sys.exit(0 if success else 1)