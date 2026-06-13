from sqlalchemy import Column, Integer, String, Index
from app.models.base import Base
from sqlalchemy.orm import relationship


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    credit = Column(Integer, nullable=False)

    __table_args__ = (
        Index('idx_name_credit', 'name', 'credit'),
    )

    enrollments = relationship(
        "Enrollment",
        back_populates="course"
    )
    assignments = relationship(
        "Assignment",
        back_populates="course",
        cascade="all, delete-orphan"
    )
