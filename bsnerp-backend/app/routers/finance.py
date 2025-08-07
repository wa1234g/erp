from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import datetime
from ..models.finance import Transaction, TransactionCreate, TransactionUpdate, Category, Invoice
from ..database import db
from ..auth.dependencies import get_current_active_user

router = APIRouter(prefix="/finance", tags=["Finance"])

@router.get("/transactions", response_model=dict)
async def get_transactions(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    type: Optional[str] = None,
    status: Optional[str] = None,
    category_id: Optional[int] = None,
    current_user: dict = Depends(get_current_active_user)
):
    transactions = list(db.transactions.values())
    
    if type:
        transactions = [t for t in transactions if t["type"] == type]
    
    if status:
        transactions = [t for t in transactions if t["status"] == status]
    
    if category_id:
        transactions = [t for t in transactions if t.get("category_id") == category_id]
    
    total = len(transactions)
    start = (page - 1) * limit
    end = start + limit
    transactions = transactions[start:end]
    
    for transaction in transactions:
        if transaction.get("category_id"):
            category = db.categories.get(transaction["category_id"])
            transaction["category_name"] = category["name"] if category else "غير محدد"
        
        if transaction.get("client_id"):
            client = db.clients.get(transaction["client_id"])
            transaction["client_name"] = client["name"] if client else "غير محدد"
    
    return {
        "transactions": transactions,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }

@router.post("/transactions", response_model=Transaction)
async def create_transaction(
    transaction_data: TransactionCreate,
    current_user: dict = Depends(get_current_active_user)
):
    transaction_id = db._get_next_id('transactions')
    now = datetime.now()
    
    transaction = {
        "id": transaction_id,
        **transaction_data.dict(),
        "status": "pending",
        "receipt_file": None,
        "parent_transaction_id": None,
        "approved_by": None,
        "approved_at": None,
        "created_at": now,
        "updated_at": now
    }
    
    db.transactions[transaction_id] = transaction
    return transaction

@router.put("/transactions/{transaction_id}", response_model=Transaction)
async def update_transaction(
    transaction_id: int,
    transaction_data: TransactionUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    transaction = db.transactions.get(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="المعاملة غير موجودة")
    
    update_data = transaction_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        transaction[key] = value
    
    transaction["updated_at"] = datetime.now()
    db.transactions[transaction_id] = transaction
    return transaction

@router.post("/transactions/{transaction_id}/approve")
async def approve_transaction(
    transaction_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    transaction = db.transactions.get(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="المعاملة غير موجودة")
    
    transaction["status"] = "approved"
    transaction["approved_by"] = current_user["id"]
    transaction["approved_at"] = datetime.now()
    transaction["updated_at"] = datetime.now()
    
    db.transactions[transaction_id] = transaction
    return {"message": "تم اعتماد المعاملة بنجاح"}

@router.get("/categories", response_model=List[Category])
async def get_categories(current_user: dict = Depends(get_current_active_user)):
    return list(db.categories.values())

@router.post("/categories", response_model=Category)
async def create_category(
    name: str,
    type: str,
    color: Optional[str] = None,
    icon: Optional[str] = None,
    current_user: dict = Depends(get_current_active_user)
):
    category_id = db._get_next_id('categories')
    now = datetime.now()
    
    category = {
        "id": category_id,
        "name": name,
        "type": type,
        "parent_id": None,
        "color": color,
        "icon": icon,
        "budget_limit": None,
        "created_at": now
    }
    
    db.categories[category_id] = category
    return category

@router.get("/reports/profit-loss")
async def get_profit_loss_report(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user: dict = Depends(get_current_active_user)
):
    transactions = list(db.transactions.values())
    
    if start_date:
        start = datetime.fromisoformat(start_date)
        transactions = [t for t in transactions if 
                       datetime.fromisoformat(t["transaction_date"].replace('Z', '+00:00')) >= start]
    
    if end_date:
        end = datetime.fromisoformat(end_date)
        transactions = [t for t in transactions if 
                       datetime.fromisoformat(t["transaction_date"].replace('Z', '+00:00')) <= end]
    
    income = sum(t["amount"] for t in transactions if t["type"] == "income" and t["status"] == "approved")
    expenses = sum(t["amount"] for t in transactions if t["type"] == "expense" and t["status"] == "approved")
    profit = income - expenses
    
    return {
        "income": income,
        "expenses": expenses,
        "profit": profit,
        "profit_margin": (profit / income * 100) if income > 0 else 0
    }

@router.get("/reports/cash-flow")
async def get_cash_flow_report(
    months: int = Query(12, ge=1, le=24),
    current_user: dict = Depends(get_current_active_user)
):
    from datetime import datetime, timedelta
    import calendar
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=months * 30)
    
    transactions = [t for t in db.transactions.values() if 
                   datetime.fromisoformat(t["transaction_date"].replace('Z', '+00:00')) >= start_date and
                   t["status"] == "approved"]
    
    monthly_data = {}
    for i in range(months):
        month_start = end_date - timedelta(days=(months - i) * 30)
        month_end = end_date - timedelta(days=(months - i - 1) * 30)
        month_key = month_start.strftime("%Y-%m")
        
        month_transactions = [t for t in transactions if 
                            month_start <= datetime.fromisoformat(t["transaction_date"].replace('Z', '+00:00')) < month_end]
        
        income = sum(t["amount"] for t in month_transactions if t["type"] == "income")
        expenses = sum(t["amount"] for t in month_transactions if t["type"] == "expense")
        
        monthly_data[month_key] = {
            "month": month_start.strftime("%B %Y"),
            "income": income,
            "expenses": expenses,
            "net": income - expenses
        }
    
    return {"monthly_data": list(monthly_data.values())}

@router.get("/stats/overview")
async def get_finance_stats(current_user: dict = Depends(get_current_active_user)):
    transactions = list(db.transactions.values())
    approved_transactions = [t for t in transactions if t["status"] == "approved"]
    
    total_income = sum(t["amount"] for t in approved_transactions if t["type"] == "income")
    total_expenses = sum(t["amount"] for t in approved_transactions if t["type"] == "expense")
    net_profit = total_income - total_expenses
    
    pending_transactions = len([t for t in transactions if t["status"] == "pending"])
    
    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_profit": net_profit,
        "pending_transactions": pending_transactions,
        "profit_margin": (net_profit / total_income * 100) if total_income > 0 else 0
    }
