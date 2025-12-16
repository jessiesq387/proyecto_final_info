from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from .models import Comentario
from .forms import ComentarioForm
from apps.articulo.models import Articulo
from apps.usuario.models import Usuario


class ComentarArticuloView(LoginRequiredMixin, View):
    def get(self, request, id):
        articulo = get_object_or_404(Articulo, id=id)
        form = ComentarioForm()
        return render(request, 'comentario/comentar.html', {'form': form, 'articulo': articulo})

    def post(self, request, id):
        articulo = get_object_or_404(Articulo, id=id)
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.articulo = articulo
            comentario.usuario = request.user
            comentario.save()
            return redirect('leer_articulo', id=id)
        return render(request, 'comentario/comentar.html', {'form': form, 'articulo': articulo})


class ListadoComentarioView(View):
    model = Comentario
    template_name = 'comentario/listadoComentario.html'
    context_object_name = 'comentarios'

    def get_queryset(self):
        user = self.request.user
        qs = Comentario.objects.select_related('usuario', 'articulo')

        # Admin ve todo
        if user.is_superuser:
            return qs

        # Colaborador: todos menos los del admin
        if user.groups.filter(name='Colaborador').exists():
            return qs.exclude(usuario__is_superuser=True)

        # Usuario normal: solo los propios
        return qs.filter(usuario=user)


class AgregarComentarioView(View):
    def get(self, request):
        usuario = Usuario(usuario=request.user)
        form = ComentarioForm()
        context = {
            'form': form,
            'usuario': usuario,
        }
        return render(request, 'comentario/agregarComentario.html', context)

    def post(self, request):
        usuario = Usuario(usuario=request.user)
        form = ComentarioForm(request.POST)
        if form.is_valid():
            form.save()
            form = ComentarioForm()
        context = {
            'form': form,
            'usuario': usuario,
        }
        return render(request, 'comentario/agregarComentario.html', context)
    

#Comentario modificación
class ComentarioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'comentario/modificar_comentario.html'

    def test_func(self):
        user = self.request.user
        comentario = self.get_object()

        if user.is_superuser:
            return True
        
        if hasattr(comentario, 'usuario') and comentario.usuario.is_superuser:
            return False
        
        if user.groups.filter(name='Colaborador').exists():
            return True
        
        return comentario.usuario == user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '¡Comentario modificado con éxito!')
        return response

    def get_success_url(self):
        articulo_id = self.object.articulo.id
        comentario_id = self.object.id
        return reverse('apps.articulo:articulo_detalle', kwargs={'id': articulo_id}) + f'#comentario-{comentario_id}'


class DeleteComentario(DeleteView):
    model = Comentario
    template_name = 'comentario/eliminarComentario.html'
    
    def get_success_url(self):
        messages.success(self.request, '¡Borrado con éxito!')
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy('apps.articulo:articulos')


class DetalleArticuloView(View):
    def get(self, request, articulo_id):
        articulo = Articulo.objects.get(id=articulo_id)
        comentarios = Comentario.objects.filter(articulo=articulo)
        return render(request, 'detalle_articulo.html', {'articulo': articulo, 'comentarios': comentarios})
