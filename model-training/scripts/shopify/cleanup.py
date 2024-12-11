import products
import categories
from tqdm import tqdm

def run():
    all_products = products.get_all_products()
    print(f"Total products in the store: {len(all_products)}")

    if len(all_products) > 0:
        for product in tqdm(all_products):
            products.delete_product_by_id(product['id'])

    all_categories = categories.get_all_categories()
    print(f"Total categories in the store: {len(all_categories)}")

    if len(all_categories) > 0:
        for category in tqdm(all_categories):
            categories.delete_category_by_id(category['id'])

if __name__ == '__main__':
    run()
