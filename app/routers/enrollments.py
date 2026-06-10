from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.user import User
from app.routers.auth import get_current_user
from app.schemas.enrollment_schemas import EnrollmentResponse

router = APIRouter(
    prefix="/enrollments",
    tags=["enrollments"]
)

@router.post(
    "/{course_id}",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED
)
def enroll_in_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Only students may enroll
    if current_user.role != "student":
        raise HTTPException(
            status_code=403,
            detail="Only students can enroll in courses"
        )

    # Course must exist
    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    # Prevent duplicate enrollment
    existing = db.query(Enrollment).filter(
        Enrollment.student_id == current_user.id,
        Enrollment.course_id == course_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Student already enrolled in this course"
        )

    new_enrollment = Enrollment(
        student_id=current_user.id,
        course_id=course_id
    )

    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)

    return new_enrollment
