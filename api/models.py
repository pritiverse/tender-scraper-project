from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class TenderDates(BaseModel):
    publishedDate: Optional[str] = None
    clarificationEndDate: Optional[str] = None
    closingDate: Optional[str] = None
    openingDate: Optional[str] = None

class TenderDetails(BaseModel):
    referenceNumber: Optional[str] = None
    title: str
    issuingAuthority: Optional[str] = None
    procurementSummary: Optional[str] = None
    category: List[str] = []
    tenderValue: Optional[float] = None
    currency: Optional[str] = None
    dates: TenderDates

class EligibilityRequirement(BaseModel):
    type: str
    description: str

class ProposalFormatItem(BaseModel):
    section: str
    questionId: str
    questionText: str
    responseType: str
    isRequired: bool

class TenderResponse(BaseModel):
    tenderId: str
    sourceUrl: Optional[str] = None
    scrapedTimestamp: str
    country: str
    state: Optional[str] = None
    region: Optional[str] = None
    tenderDetails: TenderDetails
    eligibilityRequirements: List[EligibilityRequirement] = []
    proposalFormat: List[ProposalFormatItem] = []
    unstructuredData: Dict[str, str] = {}
    vectorEmbedding: Optional[List[float]] = None

class PaginationInfo(BaseModel):
    currentPage: int
    totalPages: int
    totalResults: int
    limit: int

class TenderApiResponse(BaseModel):
    status: str = "success"
    results: int
    pagination: PaginationInfo
    data: List[TenderResponse]

class TenderSearchRequest(BaseModel):
    filters: Dict[str, Any] = {}
    pagination: Dict[str, int] = {"page": 1, "limit": 10}
