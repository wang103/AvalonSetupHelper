from django.http import HttpResponse

# Home page, lists all rooms in the READY_TO_JOIN state.
def index(request):
  return HttpResponse("Hello, world")

