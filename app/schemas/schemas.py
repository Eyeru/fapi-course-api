from pydantic import BaseModel, Field, field_validator

class CourseBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Course name")
    credit: int = Field(..., ge=1, le=6, description="Credit hours (1-6)")
    
    @field_validator('name')
    def name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Course name cannot be empty')
        return v.strip()

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int
    
    class Config:
        from_attributes = True