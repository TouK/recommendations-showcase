<script>
(function() {
  function getSnowplowDuid() {
    var match = document.cookie.match(/(?:^|; )_sp_id\.[^=]+=([^;]*)/);
    if (match && match[1]) {
      var cookieParts = decodeURIComponent(match[1]).split('.');
      return cookieParts[0];
    }
    return null;
  }

  var duid = getSnowplowDuid();

  if (!duid) {
    console.log('DUID not found');
    document.getElementById('recommendations-section').innerText = 'No recommendations available.';
    return;
  }

  function fetchRecommendations() {
    var query = `
      query getRecommendations($handle: MetaobjectHandleInput!) {
        metaobject(handle: $handle) {
          fields {
            key
            references(first: 10) {
              nodes {
                ... on Product {
                  handle
                  title
                  onlineStoreUrl
                  featuredImage {
                    url
                    altText
                  }
                }
              }
            }
          }
        }
      }
    `;

    var variables = {
      handle: {
        handle: "customer-" + duid,
        type: "nu_recommendation"
      }
    };

    fetch('https://{YOUR-SHOP-ADDRESS}/api/2024-10/graphql.json', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Shopify-Storefront-Access-Token': {USE-nussknacker_fetch_recomendations-HERE}
      },
      body: JSON.stringify({ query: query, variables: variables })
    })
    .then(function(response) {
      return response.json();
    })
    .then(function(data) {
      if (data.errors) {
        console.error('GraphQL errors:', data.errors);
        document.getElementById('recommendations-section').innerText = 'No recommendations available.';
        return;
      }

      var metaobject = data.data.metaobject;
      if (!metaobject || !metaobject.fields || metaobject.fields.length === 0) {
        document.getElementById('recommendations-section').innerText = 'No recommendations available.';
        return;
      }

      var field = metaobject.fields.find(f => f.key === 'products');
      var products = [];
      if (field && field.references && field.references.nodes) {
        products = field.references.nodes;
      }

      var container = document.getElementById('recommendations-section');

      // Ensure the header is always visible
      var header = container.querySelector('.recommendations-header');
      if (!header) {
        container.innerHTML = '<h2 class="recommendations-header">You may also be interested in...</h2>';
      }

      // Add recommendations below the header
      var recommendationsGrid = container.querySelector('.recommendations-grid');
      if (!recommendationsGrid) {
        recommendationsGrid = document.createElement('div');
        recommendationsGrid.classList.add('recommendations-grid');
        container.appendChild(recommendationsGrid);
      }

      if (products.length === 0) {
        recommendationsGrid.innerText = 'No recommendations available.';
      } else {
        var htmlContent = '';
        products.forEach(function(product) {
          htmlContent += `
            <div class="recommendation-card">
              <a href="${product.onlineStoreUrl}" class="recommendation-link">
                <img src="${product.featuredImage ? product.featuredImage.url : ''}" alt="${product.featuredImage?.altText || product.title}" class="recommendation-image">
                <h3 class="recommendation-title">${product.title}</h3>
                <button class="recommendation-button">View Product</button>
              </a>
            </div>
          `;
        });
        recommendationsGrid.innerHTML = htmlContent;
      }
    })
    .catch(function(error) {
      console.error('Error fetching recommendations:', error);
      document.getElementById('recommendations-section').innerText = 'Failed to load recommendations.';
    });
  }

  setInterval(fetchRecommendations, 3000);
  
  fetchRecommendations();
})();
</script>
