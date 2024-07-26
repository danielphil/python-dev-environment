from python_dev_environment.database import Base
from sqlalchemy.orm import mapped_column, Mapped


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
