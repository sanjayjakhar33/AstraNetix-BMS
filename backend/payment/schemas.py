from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from decimal import Decimal

# Request schemas
class PaymentRequest(BaseModel):
    user_id: str
    amount: Decimal
    currency: str = "USD"
    payment_method_type: str  # card, bank_transfer, wallet, crypto
    payment_method_id: str  # Stripe payment method ID or equivalent
    billing_period_start: Optional[str] = None  # ISO format
    billing_period_end: Optional[str] = None    # ISO format
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class InvoiceGenerationRequest(BaseModel):
    user_id: str
    billing_period_start: str  # ISO format
    billing_period_end: str    # ISO format
    include_usage_details: bool = True
    language: str = "en"
    currency: Optional[str] = None

class RefundRequest(BaseModel):
    payment_id: str
    amount: Optional[Decimal] = None  # If None, full refund
    reason: str = "requested_by_customer"
    notes: Optional[str] = None

# Response schemas
class PaymentResponse(BaseModel):
    payment_id: str
    status: str  # completed, pending, failed, blocked
    message: str
    transaction_id: Optional[str]
    amount: Decimal
    currency: str
    gateway_used: str
    fraud_score: float
    gateway_response: Optional[Dict[str, Any]] = None

class InvoiceResponse(BaseModel):
    invoice_id: str
    user_id: str
    amount_due: Decimal
    currency: str
    due_date: str  # ISO format
    invoice_data: Dict[str, Any]
    download_url: str
    payment_url: str

class BillingAnalyticsResponse(BaseModel):
    total_revenue: float
    successful_payments: int
    failed_payments: int
    pending_payments: int
    average_payment_amount: float
    payment_success_rate: float
    revenue_by_gateway: Dict[str, float]
    monthly_revenue_trend: Dict[str, float]
    churn_risk_score: float
    collection_efficiency: float
    recommendations: List[str]

class PaymentMethodResponse(BaseModel):
    id: str
    name: str
    type: str  # card, bank, wallet, crypto
    currencies: List[str]
    fees: Dict[str, float]  # percentage and fixed fees
    processing_time: str
    is_enabled: bool

class RefundResponse(BaseModel):
    refund_id: str
    status: str  # completed, pending, failed
    amount: float
    currency: str
    gateway_refund_id: str
    message: str
    estimated_completion: str