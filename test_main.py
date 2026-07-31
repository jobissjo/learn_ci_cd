import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.mark.asyncio
async def test_health_check() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "beanie-crud-api"}


@pytest.mark.asyncio
async def test_crud_operations() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        try:
            # Create
            create_res = await ac.post(
                "/items/",
                json={
                    "title": "Test Laptop",
                    "description": "CI CD Test",
                    "price": 999.99,
                },
            )
        except Exception:  # noqa: BLE001
            pytest.skip("MongoDB database connection unavailable")

        if create_res.status_code >= 500:
            pytest.skip("MongoDB database connection unavailable")

        assert create_res.status_code == 201
        data = create_res.json()
        item_id = data["id"]
        assert data["title"] == "Test Laptop"

        # Read All
        get_all_res = await ac.get("/items/")
        assert get_all_res.status_code == 200
        assert len(get_all_res.json()) >= 1

        # Read One
        get_one_res = await ac.get(f"/items/{item_id}")
        assert get_one_res.status_code == 200
        assert get_one_res.json()["title"] == "Test Laptop"

        # Update
        update_res = await ac.put(
            f"/items/{item_id}",
            json={"price": 899.99, "is_available": False},
        )
        assert update_res.status_code == 200
        assert update_res.json()["price"] == 899.99
        assert update_res.json()["is_available"] is False

        # Delete
        delete_res = await ac.delete(f"/items/{item_id}")
        assert delete_res.status_code == 204

        # Read after Delete (404)
        get_after_delete = await ac.get(f"/items/{item_id}")
        assert get_after_delete.status_code == 404
