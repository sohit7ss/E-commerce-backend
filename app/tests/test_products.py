# app/tests/test_products.py

def test_create_product(authorized_client):
    response = authorized_client.post("/product/", json={
        "Name": "Test Pen",
        "Description": "A pen for testing",
        "Price": 10,
        "StockQuantity": 5,
        "CategoryID": 1
    })
    assert response.status_code == 403   # newly registered user is "customer", not "admin"


def test_get_all_products(client):
    response = client.get("/product/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_product_unauthenticated(client):
    response = client.post("/product/", json={
        "Name": "Test Pen",
        "Description": "A pen for testing",
        "Price": 10,
        "StockQuantity": 5,
        "CategoryID": 1
    })
    assert response.status_code == 401


def test_create_product_as_customer(authorized_client):
    response = authorized_client.post("/product/", json={
        "Name": "Test Pen",
        "Description": "A pen for testing",
        "Price": 10,
        "StockQuantity": 5,
        "CategoryID": 1
    })
    assert response.status_code == 403

def test_get_nonexistent_product(client):
    response = client.get("/product/999")
    assert response.status_code == 404