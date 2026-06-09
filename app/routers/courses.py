from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.models.course import Course
from app.models.user import User
from app.schemas.course_schemas import (
    CourseCreate,
    CourseResponse
)
from app.routers.auth import require_admin

router = APIRouter(
    prefix="/courses",
    tags=["courses"]
)

@router.post(
    "",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED
)
def add_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    new_course = Course(
        name=course.name,
        credit=course.credit
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course


@router.get("", response_model=list[CourseResponse])
def get_all_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return courses


@router.get("/search", response_model=list[CourseResponse])
def search_course(
    name: str,
    db: Session = Depends(get_db)
):
    courses = db.query(Course).filter(
        Course.name.contains(name)
    ).all()

    return courses


@router.get("/{course_id}", response_model=CourseResponse)
def get_course(
    course_id: int,
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course

@router.delete("/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if course:
        db.delete(course)
        db.commit()
        return {"message": "Course deleted"}

    raise HTTPException(
        status_code=404,
        detail="Course not found"
    )


@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    updated_course: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    course.name = updated_course.name
    course.credit = updated_course.credit

    db.commit()
    db.refresh(course)

    return course
