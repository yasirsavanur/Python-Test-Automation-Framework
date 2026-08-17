"""Contract coverage for the demo catalogue API."""

import pytest

from automation_framework.api_client import ApiClient


@pytest.mark.api
@pytest.mark.smoke
def test_health_contract(api_client: ApiClient) -> None:
    response = api_client.get("/api/health")

    assert response.status_code == 200
    assert response.body == {"status": "ok", "service": "orbit-qa-store"}
    assert response.headers["Content-Type"].startswith("application/json")


@pytest.mark.api
@pytest.mark.regression
def test_product_catalog_contract(api_client: ApiClient) -> None:
    response = api_client.get("/api/products")
    products = response.body["products"]

    assert response.status_code == 200
    assert response.body["count"] == len(products) == 3
    assert len({product["id"] for product in products}) == len(products)
    assert all(product["price"] > 0 for product in products)
    assert {product["currency"] for product in products} == {"USD"}
