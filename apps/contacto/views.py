from .forms import ContactoForm
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render

class ContactoUsuario(CreateView):
    template_name = 'contacto.html'
    form_class = ContactoForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        messages.success(self.request, 'Consulta enviada.')
        return super().form_valid(form)

        from django.shortcuts import render

def acerca_de_nosotros(request):
    return render(request, 'acerca_de_nosotros.html')

