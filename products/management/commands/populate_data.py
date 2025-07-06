from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decimal import Decimal
import random

from products.models import Product, Category

User = get_user_model()

CATEGORY_TYPES = [
    ('BOOK', 'Book'),
    ('CLOTH', 'Clothing'),
    ('ELEC', 'Electronics'),
    ('FURN', 'Furniture'),
    ('TOYS', 'Toys'),
    ('SPORT', 'Sports Equipment'),
    ('MISC', 'Miscellaneous'),
    ('OTHER', 'Other'),
    ('VEHICLE', 'Vehicle'),
    ('JEWELRY', 'Jewelry'),
    ('HOME', 'Home Appliances'),
    ('GARDEN', 'Garden Supplies'),
    ('TOOLS', 'Tools'),
    ('ART', 'Art & Collectibles'),
    ('PETS', 'Pet Supplies'),
]

SAMPLE_PRODUCTS = {
    'BOOK': ['Python for Beginners', 'Django Unleashed'],
    'CLOTH': ['Blue T-Shirt', 'Winter Jacket'],
    'ELEC': ['Bluetooth Speaker', 'Smartphone'],
    'FURN': ['Office Chair', 'Bookshelf'],
    'TOYS': ['Lego Set', 'Teddy Bear'],
    'SPORT': ['Football', 'Yoga Mat'],
    'MISC': ['Gift Card', 'Surprise Box'],
    'OTHER': ['Mystery Box'],
    'VEHICLE': ['Electric Scooter'],
    'JEWELRY': ['Gold Necklace', 'Silver Ring'],
    'HOME': ['Microwave Oven', 'Washing Machine'],
    'GARDEN': ['Garden Shovel', 'Watering Can'],
    'TOOLS': ['Cordless Drill', 'Hammer'],
    'ART': ['Canvas Painting', 'Antique Vase'],
    'PETS': ['Dog Leash', 'Cat Toy'],
}

category_image_map = {
    'BOOK': 'https://res.cloudinary.com/demo/image/upload/v1699878984/sample_book.jpg',
    'CLOTH': 'https://res.cloudinary.com/demo/image/upload/v1699878984/sample_clothing.jpg',
    'ELEC': 'https://res.cloudinary.com/demo/image/upload/v1699878984/sample_electronics.jpg',
    'FURN': 'https://res.cloudinary.com/demo/image/upload/v1699878984/sample_furniture.jpg',
    'TOYS': 'https://res.cloudinary.com/demo/image/upload/v1699878984/sample_toys.jpg',
    'SPORT': 'https://res.cloudinary.com/demo/image/upload/v1699878984/sample_sports.jpg',
    'MISC': 'https://res.cloudinary.com/demo/image/upload/v1699878984/sample_misc.jpg',
    'OTHER': 'https://res.cloudinary.com/demo/image/upload/v1699878984/sample_other.jpg',
    'VEHICLE': 'https://res.cloudinary.com/demo/image/upload/v1699878984/sample_vehicle.jpg',
    'JEWELRY': 'https://res.cloudinary.com/demo/image/upload/v1699878984/sample_jewelry.jpg',
    'HOME': 'https://res.cloudinary.com/demo/image/upload/v1699878984/sample_home.jpg',
    'GARDEN': 'https://res.cloudinary.com/demo/image/upload/v1699878984/sample_garden.jpg',
    'TOOLS': 'https://res.cloudinary.com/demo/image/upload/v1699878984/sample_tools.jpg',
    'ART': 'https://res.cloudinary.com/demo/image/upload/v1699878984/sample_art.jpg',
    'PETS': 'https://res.cloudinary.com/demo/image/upload/v1699878984/sample_pets.jpg',
}

class Command(BaseCommand):
    help = 'Populates the database with categories, a demo seller, and sample products with images.'

    def handle(self, *args, **kwargs):
        # Create demo seller
        seller, created = User.objects.get_or_create(
            username='demo_seller',
            defaults={'email': 'demo@example.com'}
        )
        if created:
            seller.set_password('demo12345')
            seller.save()
            self.stdout.write("✅ Created demo seller: demo_seller")

        # Create categories
        self.stdout.write("📁 Creating categories...")
        for code, label in CATEGORY_TYPES:
            Category.objects.get_or_create(name=code)
            self.stdout.write(f"  - {label}")

        # Create products
        self.stdout.write("\n📦 Creating products...")
        for code, product_names in SAMPLE_PRODUCTS.items():
            category = Category.objects.get(name=code)
            for name in product_names:
                Product.objects.create(
                    seller=seller,
                    product_name=name,
                    description=f"{name} is a great example of a {category}.",
                    price=Decimal(random.randint(1000, 9999)) / 100,
                    category=category,
                    main_image=category_image_map.get(code)  # ✅ Add sample image
                )
                self.stdout.write(f"  ✔ Added: {name} under {category}")

        self.stdout.write(self.style.SUCCESS("🎉 Database populated with sample categories and products!"))

