
def enrollment_query(user_id):
    return [
    {
        '$match': {
            'userId': 1
        }
    }, {
        '$lookup': {
            'from': 'enrollment',
            'localField': 'userId',
            'foreignField': 'userId',
            'as': 'enrollment'
        }
    }, {
        '$unwind': {
            'path': '$enrollment',
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$lookup': {
            'from': 'course',
            'localField': 'enrollment.courseId',
            'foreignField': 'courseId',
            'as': 'course'
        }
    }, {
        '$unwind': {
            'path': '$course',
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$sort': {
            'course.courseId': 1
        }
    }
]
