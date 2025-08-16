
from db.db_models import Brand, Product, FAQ
from db.database import SessionLocal

def save_brand_context(context: dict):
    db = SessionLocal()
    try:
        brand = Brand(name=context['brand_name'], about_text=context.get('about_text'),
                      privacy_policy=context.get('privacy_policy'), refund_policy=context.get('refund_policy'))
        db.add(brand)
        db.flush()
        for prod in context['product_catalog']:
            p = Product(
                title=prod['title'],
                price=prod.get('price'),
                url=prod.get('url'),
                image_url=prod.get('image_url'),
                is_hero= 1 if prod in context.get('hero_products', []) else 0,
                brand_id=brand.id
            )
            db.add(p)
        for faq in context.get('faqs', []):
            f = FAQ(question=faq['q'], answer=faq['a'], brand_id=brand.id)
            db.add(f)
        db.commit()
        return brand.id
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
