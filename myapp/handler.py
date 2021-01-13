from corsheaders.signals import check_request_enabled

def cors_allow_api_to_everyone(sender, request, **kwargs):
    return request.path.startswith('https://hyunho-backend.herokuapp.com')

check_request_enabled.connect(cors_allow_api_to_everyone)
