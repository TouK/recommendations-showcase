import random
from datetime import datetime, timedelta
import pandas as pd
import sys
import pickle as pkl

import interaction_rules

# builds lookup index: product name -> List[interaction id]
def validate_and_build_interactions_index(interactions, product_handle_mappings):
    missing_products = []

    index = {}
    for idx, product_group in enumerate(interactions):
        for p in product_group:
            if p not in product_handle_mappings:
                missing_products.append(p)
            if p not in index:
                index[p] = []
            index[p].append(idx)

    return (missing_products, index)

def load_inventory(filename):
    with open(filename, "rb") as f:
        return pkl.load(f)

# TODO: Possible improvements:
#   * restrict interactions with the same product
#   * randomize starting timestamp to get more interactions spread over time
#   * add a slight chance to start generating interactions with the product selected from the interaction rules (nested for loop),
#     instead of a product selected for a given interaction (outer for loop)
#   * add more interactions for the same user that are spread over time
def generate_interactions(inventory, freq_bought_together_within_cat_idx, freq_bought_together_across_cat_idx):
    products_handle_dict = inventory["title_to_handle_dict"]
    category_to_products_dict = inventory["category_to_products_dict"]
    categories = list(category_to_products_dict.keys())
    interactions = []
    users = [f"user_{i}" for i in range(1, interaction_rules.MAX_USERS)]
    time_diff = timedelta(days=30)

    for user in users:
        num_interactions = random.randint(interaction_rules.MIN_NUM_INTERACTIONS_PER_USER, interaction_rules.MAX_NUM_INTERACTIONS_PER_USER)

        for _ in range(num_interactions):
            # pick a random category
            category = random.choice(categories)

            # pick a random product in the selected category
            start_date = datetime.now() - timedelta(days=30)
            product = random.choice(category_to_products_dict[category])
            timestamp = start_date + timedelta(seconds=random.randint(0, int(time_diff.total_seconds())))
            interactions.append(['1', user, products_handle_dict[product], int(timestamp.timestamp()), category])

            num_interactions_with_the_product = random.randint(1, interaction_rules.MAX_NUM_INTERACTIONS_WITH_THE_PRODUCT)
            for _ in range(num_interactions_with_the_product):
                roll = random.random()

                if roll < interaction_rules.FREQUENTLY_BOUGHT_TOGETHER_IN_CATEGORY_PROB and product in freq_bought_together_within_cat_idx:
                    # create an interaction with a product frequently bought together in the same category
                    next_product_group_idx = random.choice(freq_bought_together_within_cat_idx[product])
                    next_product = random.choice(interaction_rules.FREQUENTLY_BOUGHT_TOGETHER_WITHIN_CATEGORY[next_product_group_idx])
                    timestamp = start_date + timedelta(seconds=random.randint(0, int(time_diff.total_seconds())))
                    interactions.append(['1', user, products_handle_dict[next_product], int(timestamp.timestamp()), category])
                elif roll < (interaction_rules.FREQUENTLY_BOUGHT_TOGETHER_ACROSS_CATEGORIES_PROB + interaction_rules.FREQUENTLY_BOUGHT_TOGETHER_IN_CATEGORY_PROB) and product in freq_bought_together_across_cat_idx:
                    # create an interaction with a product frequently bought together in the different category
                    next_product_group_idx = random.choice(freq_bought_together_across_cat_idx[product])
                    next_product = random.choice(interaction_rules.FREQUENTLY_BOUGHT_TOGETHER_ACROSS_CATEGORIES[next_product_group_idx])
                    timestamp = start_date + timedelta(seconds=random.randint(0, int(time_diff.total_seconds())))
                    interactions.append(['1', user, products_handle_dict[next_product], int(timestamp.timestamp()), category])
                else:
                    # create an interaction with a random product (should have the lowest chance of happening)
                    next_product = random.choice(category_to_products_dict[category])
                    timestamp = start_date + timedelta(seconds=random.randint(0, int(time_diff.total_seconds())))
                    interactions.append(['1', user, products_handle_dict[next_product], int(timestamp.timestamp()), category])

                # NOTE: here might be a random chance to switch the `product` with the `next_product`
    return interactions

def run(inventory_filename, dataset_filename):
    inventory = load_inventory(inventory_filename)
    products_handle_dict = inventory["title_to_handle_dict"]
    (missing_products, freq_bought_together_within_cat_idx) = validate_and_build_interactions_index(
        interaction_rules.FREQUENTLY_BOUGHT_TOGETHER_WITHIN_CATEGORY,
        products_handle_dict
    )

    if len(missing_products) > 0:
        print(f"The following products do not exist in Shopify instance: {missing_products}")
        sys.exit(0)

    (missing_products, freq_bought_together_across_cat_idx) = validate_and_build_interactions_index(
        interaction_rules.FREQUENTLY_BOUGHT_TOGETHER_ACROSS_CATEGORIES,
        products_handle_dict
    )

    if len(missing_products) > 0:
        print(f"The following products do not exist in Shopify instance: {missing_products}")
        sys.exit(0)

    interactions = generate_interactions(inventory, freq_bought_together_within_cat_idx, freq_bought_together_across_cat_idx)

    print(f"Total interactions generated: {len(interactions)}")

    interactions_df = pd.DataFrame(interactions, columns=['label', 'user', 'product', 'timestamp', 'category'])

    interactions_df.to_csv(dataset_filename, index=False, sep='\t', header=False)

    print("Interactions dataset saved in:", dataset_filename)

if __name__ == "__main__":
    if len(sys.argv) > 3 or len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <inventory_filename> [dataset_filename]")
        sys.exit(0)
    elif len(sys.argv) == 3:
        dataset_filename = sys.argv[2]
        inventory_filename = sys.argv[1]
    elif len(sys.argv) == 2:
        inventory_filename = sys.argv[1]
        dataset_filename = "interactions_" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    run(inventory_filename, dataset_filename)
