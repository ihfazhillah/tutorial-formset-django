from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from .models import Kelas, Murid
from .forms import KelasForm, MuridFormSet
# Create your views here.


def index(request):
    kelas = Kelas.objects.all()
    return render(request, 'demo/index.html', 
                  {'kelas_kelas':kelas})

def create(request):
    if request.method == "GET":
        kelas_form = KelasForm()
        murid_form_set = MuridFormSet()
        return render(request, 'demo/create_kelas.html',
                      {'kelas_form':kelas_form,
                      'murid_form':murid_form_set})
    elif request.method == "POST":
        kelas_form = KelasForm(request.POST)
        murid_form = MuridFormSet(request.POST)
        if kelas_form.is_valid() and murid_form.is_valid():
            kelas_nama = kelas_form.cleaned_data['nama']
            kelas = Kelas.objects.create(nama=kelas_nama)

            for muridform in murid_form:
                if muridform.cleaned_data:
                    muridform_namadepan = muridform.cleaned_data['namadepan']
                    muridform_namabelakang = muridform.cleaned_data['namabelakang']
                    kelas.murid.create(namadepan=muridform_namadepan,
                                       namabelakang=muridform_namabelakang)

            return redirect(reverse('semua_kelas'))

def detail(request, pk):
    # kelas = Kelas.objects.get(pk=pk)
    kelas = get_object_or_404(Kelas, pk=pk)
    murids = kelas.murid.all()
    return render(request, 'demo/kelas_detail.html',
                  {'kelas':kelas,
                  'murids':murids})

def edit(request, pk):
    kelas = get_object_or_404(Kelas, pk=pk)
    initial_kelas = {'nama':kelas.nama}
    initial_murid = [{'namadepan':murid.namadepan, 
                'namabelakang':murid.namabelakang} for murid in kelas.murid.all()]
    if request.method == "POST":
        kelas_form = KelasForm(initial=initial_kelas,
                               data=request.POST)
        murid_form = MuridFormSet(initial=initial_murid,
                                  data=request.POST)
        if kelas_form.is_valid() and murid_form.is_valid():
            kelas_nama = kelas_form.cleaned_data['nama']
            kelas.nama = kelas_nama
            kelas.save()
            murid = kelas.murid.all()
            for murid in murid:
                murid.delete()
            for murid in murid_form:
                if murid.cleaned_data:
                    nama_depan = murid.cleaned_data['namadepan']
                    nama_belakang = murid.cleaned_data['namabelakang']
                    kelas.murid.create(namadepan=nama_depan,
                                       namabelakang=nama_belakang)
            return redirect(reverse('kelas_detail', args=[kelas.pk]))
    kelas_form = KelasForm(initial=initial_kelas)
    murid_form = MuridFormSet(initial=initial_murid)
    return render(request, 'demo/edit_kelas.html',
                  {'kelas_form':kelas_form,
                  'murid_form':murid_form,
                  'kelas':kelas})