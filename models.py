from pydantic import BaseModel


class Category(BaseModel):
    id: int
    name: str


class Item(BaseModel):
    address: str
    category: Category
    id: int
    price: int
    status: str
    title: str
    url: str


class Meta(BaseModel):
    page: int
    per_page: int


class ItemsResponse(BaseModel):
    meta: Meta
    resources: list[Item]