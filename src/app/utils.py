def get_status_code(status_msg: str) -> int:
    """
    Returns the status code based on the status message.
    """
    return {
        "Error": 500,
        "Created": 201,
        "Not Found": 404,
        "OK": 200
    }.get(status_msg, 500)


def rollback_with_error(session, error):
    """
    Rollback a session and raise an error.
    """
    session.rollback()
    print(error)