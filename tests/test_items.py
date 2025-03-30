import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# テスト用のデータベース設定
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def test_db():
    # テスト用のデータベースを作成
    Base.metadata.create_all(bind=engine)
    yield
    # テスト後にデータベースをクリーンアップ
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def client(test_db):
    # テスト用の依存関係を上書き
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides = {}

def test_create_item(client):
    response = client.post(
        "/items/",
        json={"name": "テストアイテム", "price": 100.0, "description": "テスト用です"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "テストアイテム"
    assert data["price"] == 100.0
    assert "id" in data
    item_id = data["id"]
    
    # 作成したアイテムを取得して確認
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json() == data

def test_read_items(client):
    # アイテムを作成
    client.post("/items/", json={"name": "アイテム1", "price": 100.0})
    client.post("/items/", json={"name": "アイテム2", "price": 200.0})
    
    # アイテム一覧を取得
    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "アイテム1"
    assert data[1]["name"] == "アイテム2"

def test_update_item(client):
    # アイテムを作成
    response = client.post(
        "/items/",
        json={"name": "旧アイテム", "price": 100.0}
    )
    item_id = response.json()["id"]
    
    # アイテムを更新
    response = client.put(
        f"/items/{item_id}",
        json={"name": "新アイテム", "price": 200.0}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "新アイテム"
    assert data["price"] == 200.0
    
    # 更新されたことを確認
    response = client.get(f"/items/{item_id}")
    assert response.json()["name"] == "新アイテム"

def test_delete_item(client):
    # アイテムを作成
    response = client.post(
        "/items/",
        json={"name": "削除アイテム", "price": 100.0}
    )
    item_id = response.json()["id"]
    
    # アイテムを削除
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 204
    
    # 削除されたことを確認
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 404