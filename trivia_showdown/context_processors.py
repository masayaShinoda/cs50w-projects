def site_info_metadata(request):
    site_title = "Trivia Showdown"
    
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
        

    return {
        "site_title": site_title,
        "user": user
    }