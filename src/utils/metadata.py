from typing import Any

from sqlalchemy import inspect
from sqlalchemy.orm import declarative_base


DeclarativeBase = declarative_base()


class Base(DeclarativeBase):
    __abstract__ = True
    repr_cols_num: int = 3
    repr_cols: tuple[str, ...] = ()

    @classmethod
    def get_subconto_mappings(cls) -> dict[Any, dict[str, None]]:
        """
        Returns all subconto fields with their ID and Type.

        Example:
            {
                "subconto_kt": {"id": "subconto_kt_id", "type": "subconto_kt_type"},
                "subconto_dt": {"id": "subconto_dt_id", "type": "subconto_dt_type"},
            }
        """

        columns = inspect(cls).columns.keys()
        subconto_fields = {}

        for column in columns:
            if "subconto" in column:
                base_name = column.rsplit("_", 1)[
                    0
                ]  # get 'subconto_' without _id/_type
                if base_name not in subconto_fields:
                    subconto_fields[base_name] = {"id": None, "type": None}
                if column.endswith("_id"):
                    subconto_fields[base_name]["id"] = column
                elif column.endswith("_type"):
                    subconto_fields[base_name]["type"] = column

        return {k: v for k, v in subconto_fields.items() if v["id"] and v["type"]}

    def __repr__(self) -> str:
        cols: list[str] = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


CoreDeclarativeBase = declarative_base()


class CoreBase(CoreDeclarativeBase):
    __abstract__ = True
    repr_cols_num: int = 3
    repr_cols: tuple[str, ...] = ()

    @classmethod
    def get_subconto_mappings(cls) -> dict[Any, dict[str, None]]:
        """
        Returns all subconto fields with their ID and Type.

        Example:
            {
                "subconto_kt": {"id": "subconto_kt_id", "type": "subconto_kt_type"},
                "subconto_dt": {"id": "subconto_dt_id", "type": "subconto_dt_type"},
            }
        """

        columns = inspect(cls).columns.keys()
        subconto_fields = {}

        for column in columns:
            if "subconto" in column:
                base_name = column.rsplit("_", 1)[
                    0
                ]  # get 'subconto_' without _id/_type
                if base_name not in subconto_fields:
                    subconto_fields[base_name] = {"id": None, "type": None}
                if column.endswith("_id"):
                    subconto_fields[base_name]["id"] = column
                elif column.endswith("_type"):
                    subconto_fields[base_name]["type"] = column

        return {k: v for k, v in subconto_fields.items() if v["id"] and v["type"]}

    def __repr__(self) -> str:
        cols: list[str] = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"
