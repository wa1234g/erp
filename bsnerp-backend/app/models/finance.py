from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"

class TransactionStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    PAID = "paid"
    CANCELLED = "cancelled"

class RecurrencePattern(str, Enum):
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"

class PaymentMethod(str, Enum):
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"
    CREDIT_CARD = "credit_card"
    PAYPAL = "paypal"
    CHECK = "check"
    OTHER = "other"

class InvoiceStatus(str, Enum):
    DRAFT = "draft"
    SENT = "sent"
    VIEWED = "viewed"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"

class Category(BaseModel):
    id: Optional[int] = None
    name: str
    type: TransactionType
    parent_id: Optional[int] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    budget_limit: Optional[float] = None
    created_at: datetime

class Transaction(BaseModel):
    id: Optional[int] = None
    type: TransactionType
    amount: float
    currency: str = "EGP"
    description: str
    category_id: Optional[int] = None
    project_id: Optional[int] = None
    client_id: Optional[int] = None
    invoice_id: Optional[int] = None
    status: TransactionStatus = TransactionStatus.PENDING
    payment_method: PaymentMethod
    reference_number: Optional[str] = None
    receipt_file: Optional[str] = None
    notes: Optional[str] = None
    tags: List[str] = []
    recurring: bool = False
    recurrence_pattern: RecurrencePattern = RecurrencePattern.NONE
    recurrence_end_date: Optional[datetime] = None
    parent_transaction_id: Optional[int] = None
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    transaction_date: datetime
    created_at: datetime
    updated_at: datetime

class Invoice(BaseModel):
    id: Optional[int] = None
    invoice_number: str
    client_id: int
    project_id: Optional[int] = None
    status: InvoiceStatus = InvoiceStatus.DRAFT
    issue_date: datetime
    due_date: datetime
    subtotal: float
    tax_rate: float = 0.0
    tax_amount: float = 0.0
    discount_rate: float = 0.0
    discount_amount: float = 0.0
    total_amount: float
    paid_amount: float = 0.0
    currency: str = "EGP"
    notes: Optional[str] = None
    terms: Optional[str] = None
    items: List[Dict[str, Any]] = []
    payments: List[int] = []
    sent_at: Optional[datetime] = None
    viewed_at: Optional[datetime] = None
    paid_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

class TransactionCreate(BaseModel):
    type: TransactionType
    amount: float
    currency: str = "EGP"
    description: str
    category_id: Optional[int] = None
    project_id: Optional[int] = None
    client_id: Optional[int] = None
    payment_method: PaymentMethod
    reference_number: Optional[str] = None
    notes: Optional[str] = None
    tags: List[str] = []
    recurring: bool = False
    recurrence_pattern: RecurrencePattern = RecurrencePattern.NONE
    recurrence_end_date: Optional[datetime] = None
    transaction_date: datetime

class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    project_id: Optional[int] = None
    client_id: Optional[int] = None
    status: Optional[TransactionStatus] = None
    payment_method: Optional[PaymentMethod] = None
    reference_number: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    transaction_date: Optional[datetime] = None
