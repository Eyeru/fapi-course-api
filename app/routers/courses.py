from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from app.models.course import Course
from app.models.user import User
from app.schemas.course_schemas import (
    CourseCreate,
    CourseResponse
)
from app.routers.auth import get_current_user, require_instructor, require_admin
from app.services.course_service import (
    get_courses,
    get_course_statistics
)

from app.schemas.stats_schemas import (
    CourseStatsResponse
)
from app.core.logger import logger

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)

@router.post(
    "",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED
)
def add_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_instructor)
):
    new_course = Course(
        name=course.name,
        credit=course.credit
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    logger.info(f"Course created: {new_course.name} (ID: {new_course.id}) by user {current_user.username}")

    return new_course


@router.get("", response_model=list[CourseResponse])
def get_all_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    credit: int | None = None,
    name: str | None = None,
    sort: str | None = None,
    db: Session = Depends(get_db),
):
    return get_courses(
        db=db,
        skip=skip,
        limit=limit,
        credit=credit,
        name=name,
        sort=sort
    )


@router.get("/search", response_model=list[CourseResponse])
def search_course(
    name: str,
    db: Session = Depends(get_db)
):
    courses = db.query(Course).filter(
        Course.name.contains(name)
    ).all()

    return courses


@router.get(
    "/stats",
    response_model=list[CourseStatsResponse]
)
def course_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    logger.info(f"Fetching course statistics by user {current_user.username}")
    return get_course_statistics(db)

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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    return course

@router.delete("/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_instructor)
):
    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if course:
        logger.info(f"Course deleted: {course.name} (ID: {course.id}) by user {current_user.username}") 
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
    current_user: User = Depends(require_instructor)
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
