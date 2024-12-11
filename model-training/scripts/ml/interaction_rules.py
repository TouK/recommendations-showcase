FREQUENTLY_BOUGHT_TOGETHER_IN_CATEGORY_PROB = 0.65
FREQUENTLY_BOUGHT_TOGETHER_ACROSS_CATEGORIES_PROB = 0.25
MAX_USERS = 150
MAX_NUM_INTERACTIONS_WITH_THE_PRODUCT = 10
MAX_NUM_INTERACTIONS_PER_USER = 100
MIN_NUM_INTERACTIONS_PER_USER = 50

assert FREQUENTLY_BOUGHT_TOGETHER_IN_CATEGORY_PROB + FREQUENTLY_BOUGHT_TOGETHER_ACROSS_CATEGORIES_PROB <= 1.0

FREQUENTLY_BOUGHT_TOGETHER_WITHIN_CATEGORY = [
    # Clothing
    ['Shirt', 'Jeans', 'Belt', 'Socks'],
    ['Sweater', 'Jacket', 'Boots'],
    ['T-shirt', 'Shorts', 'Sneakers'],
    ['Blazer', 'Trousers', 'Heels'],
    ['Hat', 'Gloves', 'Belt', 'Scarf'],

    # Electronics
    ['Smartphone', 'Charger', 'Power Bank', 'USB Cable', 'Earbuds'],
    ['Laptop', 'Keyboard', 'Mouse', 'Monitor', 'External Hard Drive'],
    ['Game Console', 'VR Headset', 'Bluetooth Speaker', 'Monitor'],
    ['Television', 'Soundbar', 'Streaming Device'],

    # Books
    ['Novel', 'Mystery', 'Thriller'],
    ['Self-help', 'Biography', 'Philosophy'],
    ['Fantasy', 'Science Fiction', 'Graphic Novel'],
    ['Textbook', 'Dictionary', 'Travel Guide'],
    ['Children’s Book', 'Comic', 'Graphic Novel'],

    # Toys
    ['Water Gun', 'Kite', 'Tricycle'],
    ['LEGO Set', 'Building Blocks'],
    ['Yo-yo', 'Rubik’s Cube', 'Slinky'],

    # Food
    ['Bread', 'Milk', 'Cereal', 'Juice', 'Coffee'],
    ['Olive Oil', 'Spices', 'Rice'],
    ['Chocolate', 'Chips', 'Biscuits'],
    ['Cheese', 'Yogurt', 'Milk'],
    ['Pizza', 'Ketchup'],
    ['Pasta', 'Cheese'],

    # Automotive Essentials
    ['Engine Oil', 'Tire', 'Spark Plug', 'Oil Filter'],
    ['Air Freshener', 'Car Mat', 'Steering Wheel Cover'],
    ['Car Jack', 'Jump Starter', 'Tire Pressure Gauge'],
    ['Car Charger', 'Dashboard Camera', 'GPS'],

    # Home Essentials
    ['Sofa', 'Coffee Table', 'Cushions', 'Lamp'],
    ['Bed', 'Wardrobe', 'Rug', 'Curtains'],
    ['Refrigerator', 'Oven', 'Microwave', 'Toaster'],
    ['Vacuum Cleaner', 'Dishwasher', 'Washing Machine'],

    # Sport
    ['Dumbbells', 'Weight Bench', 'Jump Rope', 'Yoga Mat'],
    ['Soccer Ball', 'Basketball', 'Tennis Racket', 'Running Shoes'],
    ['Bicycle', 'Helmet', 'Gloves'],
    ['Swimming Goggles', 'Towel', 'Water Bottle'],

    # Beauty
    ['Lipstick', 'Foundation', 'Mascara', 'Eyeliner'],
    ['Face Cream', 'Sunscreen', 'Serum', 'Face Mask'],
    ['Shampoo', 'Conditioner', 'Hair Dryer', 'Hair Straightener'],
    ['Body Lotion', 'Hand Cream', 'Body Wash'],

    # Health
    ['Bandages', 'Antiseptic Cream', 'Pain Reliever'],
    ['Thermometer', 'Blood Pressure Monitor', 'Oximeter'],
    ['Vitamin C', 'Multivitamin', 'Protein Powder'],
    ['Cough Syrup', 'Hand Sanitizer', 'Face Mask'],
]

FREQUENTLY_BOUGHT_TOGETHER_ACROSS_CATEGORIES = [
    # Everyday Essentials
    ['Toothbrush', 'Toothpaste', 'Shampoo', 'Soap', 'Towel', 'Face Cream', 'Coffee', 'Cereal', 'Milk'],
    ['Bread', 'Cheese', 'Juice', 'Chocolate', 'Biscuits'],
    ['Smartphone', 'Power Bank', 'Earbuds', 'Sunglasses', 'Water Bottle'],

    # Work & Study Essentials
    ['Laptop', 'Keyboard', 'Mouse', 'Monitor', 'Desk Lamp', 'Notebook', 'Coffee', 'Pen'],
    ['Textbook', 'Notebook', 'Pen', 'Highlighter', 'Backpack', 'Laptop', 'Charger'],
    ['Notebook', 'Graphic Novel', 'Tablet', 'Headphones'],

    # Travel Essentials
    ['T-shirt', 'Jeans', 'Sunglasses', 'Backpack', 'Camera', 'Travel Guide', 'Sunscreen', 'Power Bank'],
    ['Blazer', 'Trousers', 'Laptop', 'Charger', 'Smartphone', 'Power Bank', 'Notebook'],
    ['Juice', 'Car Charger', 'Jump Starter', 'Car Vacuum', 'GPS', 'Sunglasses'],

    # Fitness
    ['Running Shoes', 'Gym Shorts', 'Water Bottle', 'Protein Powder', 'Towel', 'Dumbbells'],
    ['Soccer Ball', 'Running Shoes', 'Water Bottle', 'First Aid Kit', 'Sunscreen', 'Sports Bag'],
    ['Yoga Mat', 'Dumbbells', 'Jump Rope', 'Resistance Bands'],

    # Winter Essentials
    ['Jacket', 'Sweater', 'Gloves', 'Scarf', 'Hat', 'Hand Cream'],
    ['Blanket', 'Socks', 'Thermos', 'Tea', 'Novel'],

    # Entertainment & Leisure
    ['Television', 'Bluetooth Speaker', 'Popcorn', 'Tea', 'Blanket'],
    ['Game Console', 'Headphones', 'Bluetooth Speaker'],

    # Household & Kitchen Essentials
    ['Olive Oil', 'Pasta', 'Spices', 'Garlic', 'Onion', 'Rice', 'Kitchen Knife'],
    ['Coffee Machine', 'Coffee', 'Milk', 'Sugar', 'Mug'],

    # Beauty & Personal Care
    ['Face Cream', 'Serum', 'Face Mask', 'Sunscreen', 'Makeup Remover'],
    ['Shampoo', 'Conditioner', 'Hair Dryer', 'Hairbrush', 'Hair Serum'],
    ['Foundation', 'Lipstick', 'Mascara', 'Eyeliner', 'Makeup Remover'],

    # Car & Travel Essentials
    ['First Aid Kit', 'Tire Pressure Gauge', 'Jump Starter', 'Car Charger', 'Flashlight'],

    # Health & Wellness
    ['Bandages', 'Antiseptic Cream', 'Pain Reliever', 'Thermometer'],
    ['Cough Syrup', 'Vitamin C', 'Hand Sanitizer', 'Tissues', 'Tea'],
    ['Multivitamin', 'Vitamin C', 'Protein Powder']
]
