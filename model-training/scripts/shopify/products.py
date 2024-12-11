import requests
import config

# NOTE: returns only a maximum of 250 products; this is the Shopify API constraint
def get_all_products():
    query = """
    {
      products(first: 250) {
        edges {
          node {
            id
            title
            productType
            handle
            collections(first: 100) {
              edges {
                node {
                  id
                  title
                }
              }
            }
          }
        }
      }
    }
    """

    response = requests.post(config.GRAPHQL_URL, json={'query': query}, headers=config.SHOPIFY_HEADERS)

    ret = []
    if response.status_code == 200:
        data = response.json()

        products = data["data"]["products"]["edges"]

        for product_edge in products:
            product = product_edge["node"]
            collections = product.get("collections", {}).get("edges", [])
            c = []
            if collections:
                for collection_edge in collections:
                    collection = collection_edge["node"]
                    c.append(collection['title'])

            ret.append({
                'id': product['id'],
                'title': product['title'],
                'handle': product['handle'],
                'collections': c
            })
    else:
        print(f"Response status: {response.status_code}, body: {response.text}")
    return ret

def delete_product_by_id(product_id):
    query = """
    mutation deleteProduct($id: ID!) {
      productDelete(input: {
        id: $id,
      }) {
        userErrors {
          field
          message
        }
      }
    }
    """

    variables = {
        "id": product_id,
    }
    response = requests.post(config.GRAPHQL_URL, json={'query': query, 'variables': variables}, headers=config.SHOPIFY_HEADERS)
    response_data = response.json()
    if 'userErrors' in response_data['data']['productDelete'] and response_data['data']['productDelete']['userErrors']:
        errors = response_data['data']['productDelete']['userErrors']
        for error in errors:
            print(f"Error: {error['message']}")

# TODO: improvements such as product price, product image etc
def create_product(product_name, category_id):
    query = """
    mutation createProduct($title: String!, $collectionId: ID!) {
      productCreate(input: {
        title: $title,
        collectionsToJoin: [$collectionId]
      }) {
        product {
          id
          title
        }
        userErrors {
          field
          message
        }
      }
    }
    """

    variables = {
        "title": product_name,
        "collectionId": category_id
    }

    response = requests.post(config.GRAPHQL_URL, json={'query': query, 'variables': variables}, headers=config.SHOPIFY_HEADERS)
    data = response.json()

    if "data" in data and "productCreate" in data["data"]:
        product = data["data"]["productCreate"]["product"]
        if product:
            return product['id']
        else:
            user_errors = data["data"]["productCreate"].get("userErrors", [])
            if user_errors:
                print(f"Error creating product {product_name}: {user_errors[0]['message']}")
    else:
        print(f"Error creating product: {product_name}. Response: {data}")
