from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    course_id = Column(
        Integer, 
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False
        )
    
    course = relationship("Course", back_populates="assignments")