
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from models import BrandContextRequest, BrandContextResponse
from scraper.shopify_parser import fetch_brand_insights
from db.crud import save_brand_context

app = FastAPI()

@app.post("/fetch-shopify-insights", response_model=BrandContextResponse)
async def fetch_insights(request: BrandContextRequest):
    try:
        result = fetch_brand_insights(request.website_url)
        if result is None:
            raise HTTPException(status_code=401, detail="Website not found or not a Shopify site.")
        brand_id = save_brand_context(result)  # Save to DB
        return BrandContextResponse(brand_context=result, db_id=brand_id)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
