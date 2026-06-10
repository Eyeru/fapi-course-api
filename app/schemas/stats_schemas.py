from pydantic import BaseModel


class CourseStatsResponse(BaseModel):
    course_id: int
    course_name: str
    student_count: int