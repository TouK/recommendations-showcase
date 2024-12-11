import requests
import config

def get_all_publications():
    query = '''
    {
      publications(first: 100) {
        edges {
          node {
            id
            name
          }
        }
      }
    }
    '''

    response = requests.post(
        config.GRAPHQL_URL,
        json={"query": query},
        headers=config.SHOPIFY_HEADERS
    )

    publications_dict = {}
    if response.status_code == 200:
        response_data = response.json()
        publications = response_data.get('data', {}).get('publications', {}).get('edges', [])
        if publications:
            for publication in publications:
                pub_data = publication['node']
                publications_dict[pub_data['name']] = pub_data['id']
    else:
        print(f"Failed to retrieve publications: {response.status_code}, {response.text}")
    return publications_dict

def publish_product(product_id, publication_id):
    query = '''
    mutation publishProduct($id: ID!, $input: [PublicationInput!]!) {
      publishablePublish(id: $id, input: $input) {
        userErrors {
          field
          message
        }
      }
    }
    '''

    variables = {
        "id": product_id,
        "input": {
            "publicationId": publication_id,
        }
    }

    response = requests.post(
        config.GRAPHQL_URL,
        json={"query": query, "variables": variables},
        headers=config.SHOPIFY_HEADERS
    )

    if response.status_code == 200:
        response_data = response.json()
        if 'userErrors' in response_data['data']['publishablePublish'] and response_data['data']['publishablePublish']['userErrors']:
            errors = response_data['data']['publishablePublish']['userErrors']
            for error in errors:
                print(f"Error: {error['message']}")
