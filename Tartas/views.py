from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from Tartas.forms import CakeSearchForm, AddCakeForm
from Tartas.models import Tartas

class CakeAddView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'Tartas.add_tartas'
    def get(self, request):
        form = AddCakeForm()
        return render(request, 'add_cake.html', {'form': form})

    def post(self, request):
        form = AddCakeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('add_cake'))
        return render(request, 'add_cake.html', {'form': form})


class DeleteCakeView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'Tartas.delete_tartas'
    def get(self, request, pk):
        tarta = Tartas.objects.get(pk=pk)
        return render(request, 'delete_cake.html', {'tarta': tarta})

    def post(self, request, pk):
        if request.POST['operation'] == 'Si':
            tarta = Tartas.objects.get(pk=pk)
            tarta.delete()
        return HttpResponseRedirect(reverse('add_cake'))

class UpdateCakeView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'Tartas.change_tartas'
    def get(self, request, pk):
        tarta = Tartas.objects.get(pk=pk)
        form = AddCakeForm(instance=tarta)
        return render(request, 'update_cake.html', {'form': form})

    def post(self, request, pk):
        tarta = Tartas.objects.get(pk=pk)
        form = AddCakeForm(instance=tarta, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('list_cake'))
        return render(request, 'update_cake.html', {'form': form})

class CakeListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'Tartas.view_tartas'
    def get(self, request):
        form = CakeSearchForm(request.GET)
        tartas = Tartas.objects.all()
        if form.is_valid():
            name = form.cleaned_data.get('name', '')
        else:
            name = ''
        tartas = tartas.filter(name__icontains=name)
        return render(request, 'obj_list.html', {'obj_list': tartas, 'form': form})

