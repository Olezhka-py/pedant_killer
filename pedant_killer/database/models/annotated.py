from datetime import datetime
from typing import Annotated

from sqlalchemy import func, DateTime
from sqlalchemy.orm import mapped_column


intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
created_at = Annotated[datetime, mapped_column(DateTime(timezone=True), server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(DateTime(timezone=True),
                                               server_default=func.now(),
                                               onupdate=datetime.now)]
