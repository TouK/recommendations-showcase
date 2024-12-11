import os
import sys

SHOPIFY_STORE_URL = os.environ.get("SHOPIFY_STORE_URL")
if SHOPIFY_STORE_URL is None:
    print("SHOPIFY_STORE_URL not provided")
    sys.exit(1)

SHOPIFY_ACCESS_TOKEN = os.environ.get("SHOPIFY_ACCESS_TOKEN")
if SHOPIFY_ACCESS_TOKEN is None:
    print("SHOPIFY_ACCESS_TOKEN not provided")
    sys.exit(1)

GRAPHQL_URL = f"{SHOPIFY_STORE_URL}/admin/api/2023-10/graphql.json"

SHOPIFY_HEADERS = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN
}
