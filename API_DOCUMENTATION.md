# Building Materials Store - Complete API Documentation

## 🏗️ Overview
This document provides comprehensive documentation for the Building Materials Store API, including all CRUD operations, endpoints, request/response formats, and examples.

## 🔗 Base URL
```
http://localhost:8000/
```

## 📋 Authentication
Currently, the API uses session-based authentication. For production, consider implementing JWT or API key authentication.

## 📊 API Versions

### Version 1 (v1) - Building Materials Specific
Focused on building materials industry with specialized endpoints.

### Version 2 (v2) - RESTful Standard
Standard RESTful API design with consistent naming conventions.

---

## 🏗️ Building Materials Models API (v1)

### Material Types

#### List/Create Material Types
```http
GET /api/v1/material-types/
POST /api/v1/material-types/
```

**GET Response:**
```json
[
  {
    "id": 1,
    "title_ru": "Металл",
    "title_uz": "Metall",
    "title_eng": "Metal",
    "products_count": 25
  }
]
```

**POST Request:**
```json
{
  "title_ru": "Керамика",
  "title_uz": "Keramika",
  "title_eng": "Ceramic"
}
```

#### Get/Update/Delete Material Type
```http
GET /api/v1/material-types/{id}/
PUT /api/v1/material-types/{id}/
PATCH /api/v1/material-types/{id}/
DELETE /api/v1/material-types/{id}/
```

### Material Grades

#### List/Create Material Grades
```http
GET /api/v1/material-grades/
POST /api/v1/material-grades/
```

**Response:**
```json
[
  {
    "id": 1,
    "title_ru": "Высший сорт",
    "title_uz": "Yuqori sifat",
    "title_eng": "Premium Grade"
  }
]
```

#### Get/Update/Delete Material Grade
```http
GET /api/v1/material-grades/{id}/
PUT /api/v1/material-grades/{id}/
PATCH /api/v1/material-grades/{id}/
DELETE /api/v1/material-grades/{id}/
```

### Technical Standards

#### List/Create Technical Standards
```http
GET /api/v1/technical-standards/
POST /api/v1/technical-standards/
```

**Response:**
```json
[
  {
    "id": 1,
    "title_ru": "Стандарты GOST",
    "title_uz": "GOST standartlari",
    "title_eng": "GOST Standards",
    "standard_code": "GOST"
  }
]
```

#### Get/Update/Delete Technical Standard
```http
GET /api/v1/technical-standards/{id}/
PUT /api/v1/technical-standards/{id}/
PATCH /api/v1/technical-standards/{id}/
DELETE /api/v1/technical-standards/{id}/
```

### Application Areas

#### List/Create Application Areas
```http
GET /api/v1/application-areas/
POST /api/v1/application-areas/
```

**Response:**
```json
[
  {
    "id": 1,
    "title_ru": "Жилищное строительство",
    "title_uz": "Uy qurilishi",
    "title_eng": "Residential Construction"
  }
]
```

#### Get/Update/Delete Application Area
```http
GET /api/v1/application-areas/{id}/
PUT /api/v1/application-areas/{id}/
PATCH /api/v1/application-areas/{id}/
DELETE /api/v1/application-areas/{id}/
```

### Equipment Types

#### List/Create Equipment Types
```http
GET /api/v1/equipment-types/
POST /api/v1/equipment-types/
```

**Response:**
```json
[
  {
    "id": 1,
    "title_ru": "Сверлильные инструменты",
    "title_uz": "Burg'ulash asboblari",
    "title_eng": "Drilling Tools",
    "is_power_tool": true,
    "requires_certification": false,
    "products_count": 15
  }
]
```

#### Get/Update/Delete Equipment Type
```http
GET /api/v1/equipment-types/{id}/
PUT /api/v1/equipment-types/{id}/
PATCH /api/v1/equipment-types/{id}/
DELETE /api/v1/equipment-types/{id}/
```

### Units of Measure

#### List/Create Units of Measure
```http
GET /api/v1/units-of-measure/
POST /api/v1/units-of-measure/
```

**Response:**
```json
[
  {
    "id": 1,
    "name_ru": "Штука",
    "name_uz": "Dona",
    "name_eng": "Piece",
    "symbol": "шт"
  }
]
```

#### Get/Update/Delete Unit of Measure
```http
GET /api/v1/units-of-measure/{id}/
PUT /api/v1/units-of-measure/{id}/
PATCH /api/v1/units-of-measure/{id}/
DELETE /api/v1/units-of-measure/{id}/
```

### Manufacturers

#### List/Create Manufacturers
```http
GET /api/v1/manufacturers/
POST /api/v1/manufacturers/
```

**GET Response:**
```json
[
  {
    "id": 1,
    "name": "Bosch",
    "country_ru": "Германия",
    "website": "https://www.bosch.com",
    "products_count": 45
  }
]
```

**POST Request:**
```json
{
  "name": "Makita",
  "country_ru": "Япония",
  "country_uz": "Yaponiya",
  "country_eng": "Japan",
  "website": "https://www.makita.com"
}
```

#### Get/Update/Delete Manufacturer
```http
GET /api/v1/manufacturers/{id}/
PUT /api/v1/manufacturers/{id}/
PATCH /api/v1/manufacturers/{id}/
DELETE /api/v1/manufacturers/{id}/
```

---

## 🔨 Building Materials Products API

### List/Create Building Materials
```http
GET /api/v1/building-materials/
POST /api/v1/building-materials/
```

**GET Response (List):**
```json
[
  {
    "id": 1,
    "title_ru": "Дрель электрическая Bosch GSB 120-LI",
    "title_uz": "Elektr drill Bosch GSB 120-LI",
    "title_eng": "Electric Drill Bosch GSB 120-LI",
    "price": "25000.00",
    "stock": 15,
    "product_type": "TOOL",
    "unit_type": "ШТ",
    "is_available": true,
    "is_professional": true,
    "brand_name": "Bosch",
    "manufacturer_name": "Bosch",
    "category_name": "Электроинструменты",
    "material_type_name": null,
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

**POST Request:**
```json
{
  "title_ru": "Цемент портландский М400",
  "title_uz": "Portland tsement M400",
  "title_eng": "Portland Cement M400",
  "description_ru": "Высококачественный портландский цемент",
  "specifications_ru": "Прочность на сжатие: 40 МПа",
  "installation_guide_ru": "Смешать с водой в пропорции 1:0.5",
  "length": 500.00,
  "width": 300.00,
  "height": 100.00,
  "weight": 50.000,
  "price": "800.00",
  "cost_price": "600.00",
  "stock": 100,
  "min_stock_level": 20,
  "product_type": "MATERIAL",
  "unit_type": "КГ",
  "material_composition": "Портландский клинкер, гипс",
  "certificate_number": "CERT-2024-001",
  "fire_resistance_class": "A1",
  "environmental_class": "E1",
  "categoty_id": 2,
  "material_type_id": 3,
  "manufacturer": 1,
  "is_available": true,
  "is_professional": false,
  "requires_delivery": true
}
```

### Get/Update/Delete Building Material
```http
GET /api/v1/building-materials/{id}/
PUT /api/v1/building-materials/{id}/
PATCH /api/v1/building-materials/{id}/
DELETE /api/v1/building-materials/{id}/
```

**GET Response (Detail):**
```json
{
  "id": 1,
  "title_ru": "Цемент портландский М400",
  "title_uz": "Portland tsement M400",
  "title_eng": "Portland Cement M400",
  "description_ru": "Высококачественный портландский цемент",
  "specifications_ru": "Прочность на сжатие: 40 МПа",
  "installation_guide_ru": "Смешать с водой в пропорции 1:0.5",
  "length": "500.00",
  "width": "300.00",
  "height": "100.00",
  "weight": "50.000",
  "price": "800.00",
  "cost_price": "600.00",
  "stock": 100,
  "min_stock_level": 20,
  "product_type": "MATERIAL",
  "unit_type": "КГ",
  "material_composition": "Портландский клинкер, гипс",
  "certificate_number": "CERT-2024-001",
  "fire_resistance_class": "A1",
  "environmental_class": "E1",
  "categoty_id": {
    "id": 2,
    "title_ru": "Бетон и цемент",
    "title_uz": "Beton va tsement",
    "title_eng": "Concrete and Cement"
  },
  "manufacturer": {
    "id": 1,
    "name": "LafargeHolcim",
    "country_ru": "Швейцария",
    "products_count": 12
  },
  "material_type_id": {
    "id": 3,
    "title_ru": "Бетон",
    "title_uz": "Beton",
    "title_eng": "Concrete"
  },
  "variants": [
    {
      "id": 1,
      "variant_name_ru": "Мешок 25кг",
      "price": "400.00",
      "stock": 50,
      "sku": "CEM-M400-25KG"
    }
  ],
  "reviews": [],
  "average_rating": 0,
  "is_in_stock": true,
  "is_low_stock": false,
  "total_dimensions": 0.015,
  "profit_margin": 25.0,
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

## 🔍 Specialized Product Endpoints

### Professional Products
```http
GET /api/v1/products/professional/
```
Returns products marked as professional-grade.

### Featured Products
```http
GET /api/v1/products/featured/
```
Returns featured products.

### New Arrivals
```http
GET /api/v1/products/new-arrivals/
```
Returns recently added products.

### Products on Sale
```http
GET /api/v1/products/on-sale/
```
Returns products currently on sale.

### Low Stock Products
```http
GET /api/v1/products/low-stock/
```
Returns products with stock below minimum level.

### Out of Stock Products
```http
GET /api/v1/products/out-of-stock/
```
Returns products with zero stock.

---

## 🔍 Product Filtering

### Products by Material Type
```http
GET /api/v1/products/material-type/{material_type_id}/
```

### Products by Equipment Type
```http
GET /api/v1/products/equipment-type/{equipment_type_id}/
```

### Products by Manufacturer
```http
GET /api/v1/products/manufacturer/{manufacturer_id}/
```

---

## 📊 Statistics and Reports

### Product Statistics
```http
GET /api/v1/stats/products/
```

**Response:**
```json
{
  "total_products": 150,
  "in_stock_products": 142,
  "low_stock_products": 8,
  "professional_products": 45,
  "featured_products": 20,
  "total_categories": 10,
  "total_brands": 15,
  "total_manufacturers": 12
}
```

### Inventory Report
```http
GET /api/v1/reports/inventory/
```

**Response:**
```json
[
  {
    "product_id": 1,
    "title": "Цемент портландский М400",
    "current_stock": 5,
    "min_stock_level": 20,
    "stock_status": "Low Stock",
    "last_updated": "2024-01-15T10:30:00Z"
  }
]
```

---

## 🔄 Bulk Operations

### Bulk Update Stock
```http
POST /api/v1/bulk/update-stock/
```

**Request:**
```json
{
  "updates": [
    {
      "product_id": 1,
      "stock": 50
    },
    {
      "product_id": 2,
      "stock": 25
    }
  ]
}
```

**Response:**
```json
{
  "message": "Updated 2 products",
  "updated_products": [
    {
      "product_id": 1,
      "title": "Цемент портландский М400",
      "new_stock": 50
    },
    {
      "product_id": 2,
      "title": "Дрель электрическая",
      "new_stock": 25
    }
  ]
}
```

### Bulk Update Prices
```http
POST /api/v1/bulk/update-prices/
```

**Request:**
```json
{
  "updates": [
    {
      "product_id": 1,
      "price": "850.00"
    },
    {
      "product_id": 2,
      "price": "27000.00"
    }
  ]
}
```

---

## 🔧 Product Variants

### List/Create Product Variants
```http
GET /api/v1/product-variants/
POST /api/v1/product-variants/
```

### Get Product Variants by Product
```http
GET /api/v1/products/{product_id}/variants/
```

**Response:**
```json
[
  {
    "id": 1,
    "product_title": "Цемент портландский М400",
    "variant_name_ru": "Мешок 25кг",
    "variant_name_uz": "25kg qop",
    "variant_name_eng": "25kg Bag",
    "length": "500.00",
    "width": "300.00",
    "height": "100.00",
    "weight": "25.000",
    "color": "Серый",
    "price": "400.00",
    "stock": 50,
    "sku": "CEM-M400-25KG",
    "is_available": true
  }
]
```

---

## 📝 Error Handling

### Standard Error Response
```json
{
  "error": "Error message",
  "details": "Detailed error information",
  "status_code": 400
}
```

### Common HTTP Status Codes
- `200 OK` - Successful GET, PUT, PATCH
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Invalid request data
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## 🔍 Search and Filtering

### Search Parameters
Most list endpoints support search via query parameters:

```http
GET /api/v1/building-materials/?search=цемент
GET /api/v1/manufacturers/?search=bosch
```

### Ordering
```http
GET /api/v1/building-materials/?ordering=-created_at
GET /api/v1/building-materials/?ordering=price
```

---

## 📋 Validation Rules

### Product Validation
- `price` must be greater than 0
- `stock` cannot be negative
- `length`, `width`, `height`, `weight` must be positive if provided
- `cost_price` cannot be higher than `price`

### Required Fields
- Products: `title_ru`, `price`, `stock`, `product_type`
- Manufacturers: `name`
- Material Types: `title_ru`

---

## 🧪 Testing Examples

### Create a Building Material Product
```bash
curl -X POST http://localhost:8000/api/v1/building-materials/ \
  -H "Content-Type: application/json" \
  -d '{
    "title_ru": "Кирпич керамический",
    "price": "15.00",
    "stock": 1000,
    "product_type": "MATERIAL",
    "unit_type": "ШТ"
  }'
```

### Get Product Statistics
```bash
curl http://localhost:8000/api/v1/stats/products/
```

### Search Products
```bash
curl "http://localhost:8000/api/v1/building-materials/?search=кирпич"
```

---

## 📚 Additional Resources

- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [Building Materials Migration Guide](MIGRATION_GUIDE.md)
- [Project README](README_BUILDING_MATERIALS.md)

---

**Note**: This API is designed specifically for building materials and construction equipment stores, with specialized fields and functionality for the construction industry.