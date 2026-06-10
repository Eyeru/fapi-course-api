from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from app.models.course import Course
from app.models.enrollment import Enrollment


def get_courses(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    credit: int | None = None,
    name: str | None = None,
    sort: str | None = None
):
    query = db.query(Course)

    if credit is not None:
        query = query.filter(
            Course.credit == credit
        )

    if name:
        query = query.filter(
            Course.name.contains(name)
        )

    if sort == "name":
        query = query.order_by(Course.name)

    elif sort == "-name":
        query = query.order_by(desc(Course.name))

    elif sort == "credit":
        query = query.order_by(Course.credit)

    elif sort == "-credit":
        query = query.order_by(desc(Course.credit))

    return query.offset(skip).limit(limit).all()


def get_course_statistics(db: Session):
    results = (
        db.query(
            Course.id,
            Course.name,
            func.count(Enrollment.id)
        )
        .outerjoin(
            Enrollment,
            Course.id == Enrollment.course_id
        )
        .group_by(
            Course.id,
            Course.name
        )
        .all()
    )

    return [
        {
            "course_id": row[0],
            "course_name": row[1],
            "student_count": row[2]
        }
        for row in results
    ]
