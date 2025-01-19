from datetime import datetime
from typing import Annotated

from sqlalchemy import ForeignKey, NUMERIC, func, and_, Integer, or_, Table, Column, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pedant_killer.database.database import Base, async_session_factory, config


intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]