from django.views.generic import TemplateView


class OKView(TemplateView):
    template_name = "ok.html"
