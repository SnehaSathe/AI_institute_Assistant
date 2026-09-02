from rag import retrieve_context


COURSES = {
    "python": {
        "name": "Python Programming",
        "duration": "3 Months",
        "fee": 15000,
        "timing": "6:00 PM – 8:00 PM"
    },
    "excel": {
        "name": "Advanced Excel",
        "duration": "2 Months",
        "fee": 8000,
        "timing": "5:00 PM – 7:00 PM"
    },
    "data analytics": {
        "name": "Data Analytics",
        "duration": "4 Months",
        "fee": 22000,
        "timing": "7:00 PM – 9:00 PM"
    },
    "generative ai": {
        "name": "Generative AI",
        "duration": "3 Months",
        "fee": 18000,
        "timing": "6:30 PM – 8:30 PM"
    }
}


def search_knowledge(question: str):
    """
    Search institute documents.
    """

    return retrieve_context(question)


def get_course_info(course_name: str):
    """
    Get information about a course.
    """

    course = COURSES.get(course_name.lower())

    if not course:
        return {
            "error": "Course not found"
        }

    return course


def calculate_fee(course1: str, course2: str):
    """
    Calculate the combined fee of two courses.
    """

    course_a = COURSES.get(course1.lower())
    course_b = COURSES.get(course2.lower())

    if not course_a or not course_b:
        return {
            "error": "One or both courses were not found."
        }

    total = course_a["fee"] + course_b["fee"]

    return {
        "course_1": course_a["name"],
        "course_2": course_b["name"],
        "total": total
    }