def get_session_key(request):
    if not request.user.is_authenticated:
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        return session_key
    return None
