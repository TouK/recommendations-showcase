import requests
import config

def get_all_categories():
    query = """
    {
      collections(first: 100) {
        edges {
          node {
            id
            title
            description
            productsCount
          }
        }
      }
    }
    """
    response = requests.post(config.GRAPHQL_URL, json={'query': query}, headers=config.SHOPIFY_HEADERS)

    ret = []
    if response.status_code == 200:
        data = response.json()
        categories = data["data"]["collections"]["edges"]

        for category_edge in categories:
            category = category_edge["node"]
            ret.append({
                'id': category['id'],
                'title': category['title']
            })

    return ret

def delete_category_by_id(category_id):
    query = """
    mutation deleteCollection($id: ID!) {
      collectionDelete(input: {
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
        "id": category_id,
    }
    response = requests.post(config.GRAPHQL_URL, json={'query': query, 'variables': variables}, headers=config.SHOPIFY_HEADERS)
    response_data = response.json()
    if 'userErrors' in response_data['data']['collectionDelete'] and response_data['data']['collectionDelete']['userErrors']:
        errors = response_data['data']['collectionDelete']['userErrors']
        for error in errors:
            print(f"Error: {error['message']}")

def create_category(category_name):
    query = """
        mutation createCollection($title: String!) {
          collectionCreate(input: {
            title: $title
          }) {
            collection {
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
    variables = {"title": category_name}
    response = requests.post(config.GRAPHQL_URL, json={'query': query, 'variables': variables}, headers=config.SHOPIFY_HEADERS)
    response_data = response.json()

    if 'userErrors' in response_data['data']['collectionCreate'] and response_data['data']['collectionCreate']['userErrors']:
        errors = response_data['data']['collectionCreate']['userErrors']
        for error in errors:
            print(f"Error: {error['message']}")
