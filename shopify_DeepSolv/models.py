
from pydantic import BaseModel
from typing import List, Dict, Optional

class Product(BaseModel):
    title: str
    price: Optional[float]
    url: Optional[str]
    image_url: Optional[str] = None

class BrandContext(BaseModel):
    brand_name: Optional[str]
    hero_products: List[Product] = []
    product_catalog: List[Product] = []
    privacy_policy: Optional[str] = None
    refund_policy: Optional[str] = None
    faqs: List[Dict[str, str]] = []
    social_handles: Dict[str, str] = {}
    contact_details: Dict[str, str] = {}
    about_text: Optional[str] = None
    important_links: Dict[str, str] = {}

class BrandContextRequest(BaseModel):
    website_url: str

class BrandContextResponse(BaseModel):
    brand_context: BrandContext
    db_id: Optional[int] = None
