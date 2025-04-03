import typing
from typing import Literal

from pydantic import BaseModel
from sqlalchemy import bindparam

from src.application.transport.mixins.daterange import DaterangeMixin


def get_date_filters(
        dto: DaterangeMixin,
        *,
        filters: list[str | None] = None,
        date_field_name: str = "date",
        dto_start_date_field_name: str = "start_date",
        dto_end_date_field_name: str = "end_date",
        gt_ge: Literal['gt', 'ge'] = "ge",
        lt_le: Literal['lt', 'le'] = "le",
) -> list[str]:
    if filters is None:
        filters = []
    start_date_condition = ">=" if gt_ge == "ge" else ">"
    end_date_condition = "<=" if lt_le == "le" else "<"
    if getattr(dto, dto_start_date_field_name):
        filters.append(date_field_name+" "+start_date_condition+" :"+dto_start_date_field_name)
    if getattr(dto, dto_end_date_field_name):
        filters.append(date_field_name+" "+end_date_condition+" :"+dto_end_date_field_name)
    return filters


def apply_filters(stmt: str, filters: list[str]) -> str:
    if filters:
        return stmt + " where " + " and ".join(filters)
    return stmt


def insert_filters(filters: list[str | None]) -> str:
    if len(filters) != 0:
        return " where " + " and ".join(filters)
    return ""


def f_ilike(
    dto: BaseModel,
    filters: list,
    bindparams: list,
    column: str,
    *,
    before: bool = True,
    after: bool = True
) -> tuple[list, list]:
    value = getattr(dto, column)
    if value is not None:
        pattern = ("%" if before else "") + ":" + column + ("%" if after else "")
        if isinstance(value, typing.Sequence):
            filters.append(column + " ilike any(array[" + pattern + "])")
            bindparams.append(bindparam(column, expanding=True))
        else:
            filters.append(column + " ilike " + pattern)
            bindparams.append(bindparam(column))
    return filters, bindparams


def f_in(
    dto: BaseModel,
    filters: list,
    bindparams: list,
    column: str,
) -> tuple[list, list]:
    if getattr(dto, column) is not None:
        filters.append(column+" in :"+column)
        bindparams.append(bindparam(column, expanding=True))
    return filters, bindparams
