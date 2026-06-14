"""Customer business logic layer.

All methods accept a SQLAlchemy session and handle errors explicitly.
"""

from datetime import datetime, timezone
from typing import Optional, Tuple

from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerNotFoundError(Exception):
    """Raised when a customer is not found or already soft-deleted."""

    pass


def get_customers(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    name: Optional[str] = None,
    company: Optional[str] = None,
    status: Optional[str] = None,
    level: Optional[str] = None,
    source: Optional[str] = None,
    sort_order: Optional[str] = None,
) -> Tuple[list, int]:
    """Return a paginated list of active (non-deleted) customers with optional filters."""
    query = db.query(Customer).filter(Customer.deleted_at.is_(None))

    # Apply filters (escape LIKE wildcards to prevent injection)
    if name:
        safe = name.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        query = query.filter(Customer.name.like(f"%{safe}%"))
    if company:
        safe = company.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        query = query.filter(Customer.company.like(f"%{safe}%"))
    if status:
        query = query.filter(Customer.status == status)
    if level:
        query = query.filter(Customer.level == level)
    if source:
        query = query.filter(Customer.source == source)

    # Sorting
    if sort_order == "name_asc":
        query = query.order_by(Customer.name.asc())
    elif sort_order == "name_desc":
        query = query.order_by(Customer.name.desc())
    elif sort_order == "created_asc":
        query = query.order_by(Customer.created_at.asc())
    elif sort_order == "created_desc":
        query = query.order_by(Customer.created_at.desc())
    else:
        # Default: newest first
        query = query.order_by(Customer.created_at.desc())

    total = query.count()
    offset = (page - 1) * page_size
    items = query.offset(offset).limit(page_size).all()

    return items, total


def get_customer_by_id(db: Session, customer_id: int) -> Customer:
    """Return a single customer by ID. Raises CustomerNotFoundError if not found."""
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id, Customer.deleted_at.is_(None))
        .first()
    )
    if customer is None:
        raise CustomerNotFoundError(f"客户不存在: ID={customer_id}")
    return customer


def create_customer(db: Session, data: CustomerCreate) -> Customer:
    """Create a new customer and return it."""
    customer = Customer(**data.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def update_customer(db: Session, customer_id: int, data: CustomerUpdate) -> Customer:
    """Update an existing customer. Raises CustomerNotFoundError if not found."""
    customer = get_customer_by_id(db, customer_id)

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(customer, key, value)

    db.commit()
    db.refresh(customer)
    return customer


def soft_delete_customer(db: Session, customer_id: int) -> None:
    """Soft-delete a customer by setting deleted_at. Raises CustomerNotFoundError if not found."""
    customer = get_customer_by_id(db, customer_id)
    customer.deleted_at = datetime.now(timezone.utc)
    db.commit()
