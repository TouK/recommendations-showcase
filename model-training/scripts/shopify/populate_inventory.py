import sys
import products
import inventory
import publications
import categories
from tqdm import tqdm

ONLINE_STORE_PUBLICATION = 'Online Store'

def create_categories_id_mapping(categories):
    category_name_to_id = {}

    for category in categories:
        category_name_to_id[category['title']] = category['id']

    return category_name_to_id

def run():
    all_publications = publications.get_all_publications()
    online_store_publication_id = all_publications[ONLINE_STORE_PUBLICATION]
    if not online_store_publication_id:
        print(f"Unable to find 'Online Store' publication!")
        sys.exit(1)

    existing_categories_names = set(map(lambda category: category['title'],  categories.get_all_categories()))
    missing_categories = list(filter(lambda category: category not in existing_categories_names, inventory.CATEGORIES))

    if len(missing_categories) > 0:
        print(f"Total categories to create (after filtering): {len(missing_categories)}")
        for category in tqdm(missing_categories):
            categories.create_category(category)

    all_categories = categories.get_all_categories()
    categories_id_mapping = create_categories_id_mapping(all_categories)

    existing_products_names = set(map(lambda product: product['title'], products.get_all_products()))
    created_product_ids = []
    for category, product_list in inventory.PRODUCTS.items():
        category_id = categories_id_mapping[category]
        if not category_id:
            print(f"Category {category} has no ID mapping. Skipping...")
            continue
        missing_products = list(filter(lambda product: product not in existing_products_names, product_list))
        if len(missing_products) > 0:
            print(f"Creating products for category: {category} (ID: {category_id})")
            for product in tqdm(missing_products):
                product_id = products.create_product(product, category_id)
                created_product_ids.append(product_id)

    if len(created_product_ids) > 0:
        print("Publishing created products to 'Online Store' channel")
        for product_id in tqdm(created_product_ids):
            publications.publish_product(product_id, online_store_publication_id)

if __name__ == '__main__':
    run()
