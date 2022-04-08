from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from api.commprotocol.server_response import AUTHORIZATION_DENIED, ERROR_SERVER, MAX_FILE_SIZE, ONLY_POST_ALLOWED, WRONG_FILE, WRONG_JSON, ServerResponse
from api.services import file_service, process_service, security_service
from api.utils.constants import MAX_SIZE
# Create your views here.
@csrf_exempt
def test(request):
    """
    Returns the JSON
    {
        'test': 'hello world'
    }
    Parameters
    ----------
    request : django.core.handlers.wsgi.WSGIRequest
    """
    print(request)
    return JsonResponse({'test': 'hello world'}, safe=False)
@csrf_exempt
def upload(request):
    if request.method != 'POST':
        return JsonResponse(ServerResponse(status=ONLY_POST_ALLOWED).get(), safe=False)
    try:
        auth = request.headers["Authorization"]
    except:
        return JsonResponse(ServerResponse(status=AUTHORIZATION_DENIED).get(), safe=False)
    if security_service.get_user_from_auth(auth) is None:
        return JsonResponse(ServerResponse(status=AUTHORIZATION_DENIED).get(), safe=False)
    try:
        file = request.FILES['file']
        if file.size > MAX_SIZE:
            return JsonResponse(ServerResponse(status=MAX_FILE_SIZE).get(), safe=False)
        if file.name.rpartition('.')[-1] not in ['xls', 'xlsx', 'xlsb']:
            return JsonResponse(ServerResponse(status=WRONG_FILE).get(), safe=False)
        response = file_service.upload_file(request.POST, file)
    except:
        return JsonResponse(ServerResponse(status=WRONG_FILE).get(), safe=False)
    return JsonResponse(response.get(), safe=False)
@csrf_exempt
def pasocero(request):
    if request.method != 'POST':
        return JsonResponse(ServerResponse(status=ONLY_POST_ALLOWED).get(), safe=False)
    try:
        auth = request.headers["Authorization"]
    except:
        return JsonResponse(ServerResponse(status=AUTHORIZATION_DENIED).get(), safe=False)
    if security_service.get_user_from_auth(auth) is None:
        return JsonResponse(ServerResponse(status=AUTHORIZATION_DENIED).get(), safe=False)
    try:
        process_data = JSONParser().parse(request)
    except:
        return JsonResponse(ServerResponse(status=WRONG_JSON).get(), safe=False)
    try:
        response = process_service.pasocero(process_data)
    except:
        return JsonResponse(ServerResponse(status=ERROR_SERVER).get(), safe=False)
    return JsonResponse(response.get(), safe=False)