from django.http import HttpResponse

from django.http import HttpRequest

def test_view(request: HttpRequest) -> HttpResponse:
    """A simple test view to verify Django routing works."""
    return HttpResponse("<h1>Django Test View Works!</h1>")
