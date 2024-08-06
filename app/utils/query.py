from sqlalchemy.orm import Query
from app.schemas.query import FilterCondition, SortOrder
from sqlalchemy import and_, or_, func
from sqlalchemy.sql import text

def apply_filters(query: Query, model: any, filters: list[FilterCondition]) -> Query:
    for filter_condition in filters:
        column = getattr(model, filter_condition.field)
        operator = filter_condition.operator
        value = filter_condition.value
        data_type = filter_condition.data_type

        if data_type == 'string':
            if operator == "eq":
                query = query.filter(func.lower(column) == func.lower(value))
            elif operator == "ne":
                query = query.filter(func.lower(column) != func.lower(value))
            elif operator == "like":
                query = query.filter(func.lower(column).like(func.lower(text(f"%{value}%"))))
            elif operator == "ilike":
                query = query.filter(column.ilike(text(f"%{value}%")))
            elif operator == "in":
                query = query.filter(column.in_(value))
        elif data_type == 'number':
            if operator == "eq":
                query = query.filter(column == value)
            elif operator == "ne":
                query = query.filter(column != value)
            elif operator == "gt":
                query = query.filter(column > value)
            elif operator == "lt":
                query = query.filter(column < value)
            elif operator == "ge":
                query = query.filter(column >= value)
            elif operator == "le":
                query = query.filter(column <= value)
            elif operator == "between":
                query = query.filter(column.between(value[0], value[1]))
            elif operator == "in":
                query = query.filter(column.in_(value))
        elif data_type == 'date':
            if operator == "eq":
                query = query.filter(func.date(column) == value)
            elif operator == "ne":
                query = query.filter(func.date(column) != value)
            elif operator == "gt":
                query = query.filter(column > value)
            elif operator == "lt":
                query = query.filter(column < value)
            elif operator == "between":
                query = query.filter(column.between(value.start, value.end))
        elif data_type == 'boolean':
            query = query.filter(column.is_(value))
        elif data_type == 'enum':
            if operator == "eq":
                query = query.filter(column == value)
            elif operator == "ne":
                query = query.filter(column != value)
            elif operator == "in":
                query = query.filter(column.in_(value))

    return query

def apply_sorting(query: Query, model: any, sort_orders: list[SortOrder]) -> Query:
    for sort_order in sort_orders:
        column = getattr(model, sort_order.field)
        if sort_order.field.endswith('_date'):  # Assuming date fields end with '_date'
            column = func.date(column)
        if sort_order.direction.lower() == "desc":
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())
    
    return query