import sys

import products
import pickle as pkl

def run(filename):
    all_products = products.get_all_products()

    handle_to_id_dict = {}
    title_to_handle_dict = {}
    category_to_products_dict = {}
    for product in all_products:
        handle_to_id_dict[product["handle"]] = product["id"]
        title_to_handle_dict[product["title"]] = product["handle"]
        categories = product["collections"]
        if len(categories) > 1:
            print(f"Found categories: [${categories}] for product: ${product}. Only single category products are supported!")
            sys.exit(1)

        if len(categories) < 1:
            print(f"No categories for product ${product} found. Only products with an assigned category are supported!")
            sys.exit(1)

        category = categories[0]
        if category not in category_to_products_dict:
            category_to_products_dict[category] = []
        category_to_products_dict[category].append(product["title"]) # TODO: handle or name?
        # TODO: products duplicate checks

    inventory = {
        "handle_to_id_dict": handle_to_id_dict,
        "title_to_handle_dict": title_to_handle_dict,
        "category_to_products_dict": category_to_products_dict,
    }

    pkl.dump(inventory, open(filename, "wb"))
    print(f"Shopify products inventory saved in {filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} [filename]")
        sys.exit(0)
    else:
        run(sys.argv[1])



