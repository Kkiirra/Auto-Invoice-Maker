

def user_first_letter(request):
    if request.user.is_authenticated:
        try:
            logo_letter = request.user.first_name[0]
        except Exception:
            logo_letter = request.user.email[0]
        return {'user_logo_letter': logo_letter.upper()}
    else:
        return {}
