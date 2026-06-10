from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.user import User
from app.routers.auth import get_current_user
from app.schemas.enrollment_schemas import (
    EnrollmentResponse,
    MyCourseResponse
)

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
@router.get(
    "/me",
    response_model=list[MyCourseResponse]
)
def get_my_courses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    enrollments = db.query(Enrollment).filter(
        Enrollment.student_id == current_user.id
    ).all()

    result = []

    for enrollment in enrollments:
        result.append(
            MyCourseResponse(
                course_id=enrollment.course.id,
                course_name=enrollment.course.name,
                credit=enrollment.course.credit
            )
        )

    return result


@router.delete("/{course_id}")
def withdraw_from_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "student":
        raise HTTPException(
            status_code=403,
            detail="Only students can withdraw from courses"
        )

    enrollment = db.query(Enrollment).filter(
        Enrollment.student_id == current_user.id,
        Enrollment.course_id == course_id
    ).first()

    if not enrollment:
        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )

    db.delete(enrollment)
    db.commit()

    return {"message": "Successfully withdrawn from course"}