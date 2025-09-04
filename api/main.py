from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List
import pymongo
from bson import ObjectId
import math
from datetime import datetime

from .models import TenderApiResponse, TenderSearchRequest, TenderResponse, TenderDetails, TenderDates, PaginationInfo

app = FastAPI(title="GlobalTender API", version="1.0.0")

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["tenderdb"]
collection = db["tenders"]

def serialize_tender(tender_doc):
    """Convert MongoDB document to API format"""
    if not tender_doc:
        return None
    
    # Convert ObjectId to string
    tender_doc['_id'] = str(tender_doc['_id'])
    
    return TenderResponse(
        tenderId=tender_doc.get('tenderId', ''),
        sourceUrl=tender_doc.get('sourceUrl'),
        scrapedTimestamp=tender_doc.get('scrapedTimestamp', datetime.utcnow().isoformat() + 'Z'),
        country=tender_doc.get('country', ''),
        state=tender_doc.get('state'),
        region=tender_doc.get('region'),
        tenderDetails=TenderDetails(
            referenceNumber=tender_doc.get('tenderDetails', {}).get('referenceNumber'),
            title=tender_doc.get('tenderDetails', {}).get('title', 'No Title'),
            issuingAuthority=tender_doc.get('tenderDetails', {}).get('issuingAuthority'),
            procurementSummary=tender_doc.get('tenderDetails', {}).get('procurementSummary'),
            category=tender_doc.get('tenderDetails', {}).get('category', []),
            tenderValue=tender_doc.get('tenderDetails', {}).get('tenderValue'),
            currency=tender_doc.get('tenderDetails', {}).get('currency'),
            dates=TenderDates(
                publishedDate=tender_doc.get('tenderDetails', {}).get('dates', {}).get('publishedDate'),
                clarificationEndDate=tender_doc.get('tenderDetails', {}).get('dates', {}).get('clarificationEndDate'),
                closingDate=tender_doc.get('tenderDetails', {}).get('dates', {}).get('closingDate'),
                openingDate=tender_doc.get('tenderDetails', {}).get('dates', {}).get('openingDate')
            )
        ),
        eligibilityRequirements=tender_doc.get('eligibilityRequirements', []),
        proposalFormat=tender_doc.get('proposalFormat', []),
        unstructuredData=tender_doc.get('unstructuredData', {}),
        vectorEmbedding=tender_doc.get('vectorEmbedding')
    )

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "GlobalTender API v1.0.0", "status": "active"}

@app.get("/v1/tenders", response_model=TenderApiResponse, tags=["Tenders"])
async def get_tenders(
    country: Optional[str] = Query(None, description="ISO 3166-1 alpha-2 country code"),
    state: Optional[str] = Query(None, description="State, province, or region"),
    keywords: Optional[str] = Query(None, description="Comma-separated keywords to search in title/summary"),
    tenderId: Optional[str] = Query(None, description="Fetch a specific tender by its unique ID"),
    min_value: Optional[int] = Query(None, description="Minimum tender value"),
    currency: Optional[str] = Query(None, description="ISO 4217 currency code"),
    page: int = Query(1, description="Page number for pagination"),
    limit: int = Query(10, description="Number of results per page", le=100)
):
    # Build query filter
    query_filter = {}
    
    if country:
        query_filter['country'] = country
    if state:
        query_filter['state'] = state
    if tenderId:
        query_filter['tenderId'] = tenderId
    if min_value:
        query_filter['tenderDetails.tenderValue'] = {"$gte": min_value}
    if currency:
        query_filter['tenderDetails.currency'] = currency
    if keywords:
        keyword_list = [kw.strip() for kw in keywords.split(',')]
        query_filter['$or'] = [
            {'tenderDetails.title': {"$regex": "|".join(keyword_list), "$options": "i"}},
            {'tenderDetails.procurementSummary': {"$regex": "|".join(keyword_list), "$options": "i"}}
        ]
    
    # Calculate pagination
    skip = (page - 1) * limit
    
    # Get total count
    total_results = collection.count_documents(query_filter)
    total_pages = math.ceil(total_results / limit) if total_results > 0 else 0
    
    # Get results
    cursor = collection.find(query_filter).skip(skip).limit(limit)
    tenders = []
    
    for doc in cursor:
        serialized = serialize_tender(doc)
        if serialized:
            tenders.append(serialized)
    
    return TenderApiResponse(
        status="success",
        results=len(tenders),
        pagination=PaginationInfo(
            currentPage=page,
            totalPages=total_pages,
            totalResults=total_results,
            limit=limit
        ),
        data=tenders
    )

@app.post("/v1/tenders/search", response_model=TenderApiResponse, tags=["Tenders"])
async def search_tenders(request: TenderSearchRequest):
    query_filter = {}
    
    # Process filters
    filters = request.filters
    
    if 'location' in filters:
        location = filters['location']
        if 'country' in location:
            countries = location['country'] if isinstance(location['country'], list) else [location['country']]
            query_filter['country'] = {"$in": countries}
        if 'state' in location:
            states = location['state'] if isinstance(location['state'], list) else [location['state']]
            query_filter['state'] = {"$in": states}
    
    if 'keywords' in filters:
        keywords_filter = filters['keywords']
        include_keywords = keywords_filter.get('include', [])
        exclude_keywords = keywords_filter.get('exclude', [])
        
        if include_keywords:
            query_filter['$or'] = [
                {'tenderDetails.title': {"$regex": "|".join(include_keywords), "$options": "i"}},
                {'tenderDetails.procurementSummary': {"$regex": "|".join(include_keywords), "$options": "i"}}
            ]
        
        if exclude_keywords:
            query_filter['$and'] = [
                {'tenderDetails.title': {"$not": {"$regex": "|".join(exclude_keywords), "$options": "i"}}},
                {'tenderDetails.procurementSummary': {"$not": {"$regex": "|".join(exclude_keywords), "$options": "i"}}}
            ]
    
    if 'valueRange' in filters:
        value_range = filters['valueRange']
        value_query = {}
        if 'min' in value_range:
            value_query["$gte"] = value_range['min']
        if 'max' in value_range:
            value_query["$lte"] = value_range['max']
        if value_query:
            query_filter['tenderDetails.tenderValue'] = value_query
        if 'currency' in value_range:
            query_filter['tenderDetails.currency'] = value_range['currency']
    
    # Pagination
    pagination = request.pagination
    page = pagination.get('page', 1)
    limit = pagination.get('limit', 10)
    skip = (page - 1) * limit
    
    # Get results
    total_results = collection.count_documents(query_filter)
    total_pages = math.ceil(total_results / limit) if total_results > 0 else 0
    
    cursor = collection.find(query_filter).skip(skip).limit(limit)
    tenders = []
    
    for doc in cursor:
        serialized = serialize_tender(doc)
        if serialized:
            tenders.append(serialized)
    
    return TenderApiResponse(
        status="success",
        results=len(tenders),
        pagination=PaginationInfo(
            currentPage=page,
            totalPages=total_pages,
            totalResults=total_results,
            limit=limit
        ),
        data=tenders
    )

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
