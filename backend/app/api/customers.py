"""Customer CRUD API router.

All endpoints return the unified { code, message, data } response format.
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.customer import (
    CustomerCreate,
    CustomerListResponse,
    CustomerResponse,
    CustomerUpdate,
)
from app.schemas.response import error, success
from app.services.customer_service import (
    CustomerNotFoundError,
    create_customer,
    get_customer_by_id,
    get_customers,
    soft_delete_customer,
    update_customer,
)

router = APIRouter()


@router.post(
    "/customers",
    response_model=dict,
    status_code=201,
    operation_id="create_customer",
    summary="创建客户",
    tags=["Customers"],
)
def create_customer_endpoint(
    data: CustomerCreate,
    db: Session = Depends(get_db),
):
    """Create a new customer record."""
    try:
        customer = create_customer(db, data)
        return success(data=CustomerResponse.model_validate(customer), message="客户创建成功")
    except Exception as e:
        return error(code=500, message=f"创建客户失败: {str(e)}")


@router.get(
    "/customers",
    response_model=dict,
    status_code=200,
    operation_id="list_customers",
    summary="获取客户列表",
    tags=["Customers"],
)
def list_customers_endpoint(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    name: Optional[str] = Query(None, description="客户名称 (模糊搜索)"),
    company: Optional[str] = Query(None, description="公司名称 (模糊搜索)"),
    status: Optional[str] = Query(None, pattern=r"^(active|inactive)$", description="状态"),
    level: Optional[str] = Query(None, pattern=r"^[ABCD]$", description="客户等级"),
    source: Optional[str] = Query(None, description="客户来源"),
    sort_order: Optional[str] = Query(
        None,
        pattern=r"^(name_asc|name_desc|created_asc|created_desc)$",
        description="排序方式",
    ),
    db: Session = Depends(get_db),
):
    """Get a paginated list of customers with optional filtering and sorting."""
    try:
        items, total = get_customers(
            db=db,
            page=page,
            page_size=page_size,
            name=name,
            company=company,
            status=status,
            level=level,
            source=source,
            sort_order=sort_order,
        )

        customer_list = [CustomerResponse.model_validate(c) for c in items]

        return success(
            data={
                "items": customer_list,
                "total": total,
                "page": page,
                "page_size": page_size,
            }
        )
    except Exception as e:
        return error(code=500, message=f"获取客户列表失败: {str(e)}")


@router.get(
    "/customers/{customer_id}",
    response_model=dict,
    status_code=200,
    operation_id="get_customer",
    summary="获取客户详情",
    tags=["Customers"],
)
def get_customer_endpoint(
    customer_id: int,
    db: Session = Depends(get_db),
):
    """Get a single customer by ID."""
    try:
        customer = get_customer_by_id(db, customer_id)
        return success(data=CustomerResponse.model_validate(customer))
    except CustomerNotFoundError:
        return error(code=404, message="客户不存在")
    except Exception as e:
        return error(code=500, message=f"获取客户详情失败: {str(e)}")


@router.put(
    "/customers/{customer_id}",
    response_model=dict,
    status_code=200,
    operation_id="update_customer",
    summary="更新客户",
    tags=["Customers"],
)
def update_customer_endpoint(
    customer_id: int,
    data: CustomerUpdate,
    db: Session = Depends(get_db),
):
    """Update an existing customer. Only provided fields are updated."""
    try:
        customer = update_customer(db, customer_id, data)
        return success(data=CustomerResponse.model_validate(customer), message="客户更新成功")
    except CustomerNotFoundError:
        return error(code=404, message="客户不存在")
    except Exception as e:
        return error(code=500, message=f"更新客户失败: {str(e)}")


@router.delete(
    "/customers/{customer_id}",
    response_model=dict,
    status_code=200,
    operation_id="delete_customer",
    summary="删除客户 (软删除)",
    tags=["Customers"],
)
def delete_customer_endpoint(
    customer_id: int,
    db: Session = Depends(get_db),
):
    """Soft-delete a customer (sets deleted_at timestamp)."""
    try:
        soft_delete_customer(db, customer_id)
        return success(data=None, message="客户删除成功")
    except CustomerNotFoundError:
        return error(code=404, message="客户不存在")
    except Exception as e:
        return error(code=500, message=f"删除客户失败: {str(e)}")
