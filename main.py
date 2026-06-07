from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.responses import JSONResponse
from app.schemas.schemas import CourseCreate, CourseResponse
from app.models.course import Course
from app.routers import auth
from sqlalchemy.orm import Session
from database import get_db

app = FastAPI()

app.include_router(auth.router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "path": str(request.url)}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "path": str(request.url)}
    )


@app.get("/")
def home():
    return {"message": "Hello Backend"}


@app.get("/courses", response_model=list[CourseResponse])
def get_all_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return courses


@app.get("/courses/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):

    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(status_code=404,
                            detail="Course not found"
                            )

    return course


@app.post(
    "/courses",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_course(course: CourseCreate, db: Session = Depends(get_db)):

    new_course = Course(
        name=course.name,
        credit=course.credit
        )
    db.add(new_course)

    db.commit()

    db.refresh(new_course)

    return new_course


@app.get("/search", response_model=list[CourseResponse])
def search_course(name: str, db: Session = Depends(get_db)):
    courses = db.query(Course).filter(Course.name.contains(name)).all()

    return courses


@app.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):

    course = db.query(Course).filter(Course.id == course_id).first()
    if course:
        db.delete(course)
        db.commit()
        return {"message": "Course deleted"}

    raise HTTPException(status_code=404,
                        detail="Course not found"
                        )


@app.put("/courses/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    updated_course: CourseCreate,
    db: Session = Depends(get_db),
):

    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    course.name = updated_course.name
    course.credit = updated_course.credit

    db.commit()
    db.refresh(course)

    return course
