# Memahami Formset
Ini adalah tutorial sederhana mengenai formset dalam django.

Anda bisa mengusulkan pembenahan dalam tutorial ini bila ada kesalahan atau kekurangan. 

Ihfazhillah [mihfazhillah@gmail.com](mailto:mihfazhillah@gmail.com)

[TOC]
## Django Formset


Django formset factory, adalah modul yang memudahkan kita untuk membuat beberapa form dalam satu halaman dari satu form. Ok, misalkan `UserForm` yang sudah kita buat, kita ingin tampilkan 3 atau 4 buah di satu halaman, maka kita gunakan `formset_factory` yang berada di `django.forms`

Ok, sekarang kita akan membuat demo. Misalkan kita ingin membuat aplikasi bernama `formset_demo` yang di dalamnya ada dua tabel. 
1. Kelas
2. Murid

Nah, `murid` memiliki hubungan dengan `kelas` dengan `foreignkey`. Jadi, yang akan di buat formset adalah `murid` dan akan nempel di halaman ketika kita nambah `kelas` atau meng-edit-nya.
### Membuat Project Baru
- Buat project dengan `django-admin startproject formset_demo`
- Kemudian buat app di dalamnya dengan `./manage.py startapp demo`

Maka, tampilan pohon direktori kita akan seperti di bawah ini.

```shell
├── demo
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── formset_demo
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-34.pyc
│   │   └── settings.cpython-34.pyc
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py

4 directories, 14 files

```
### Membuat Model
- Ok, kemudian kita buat model di `models.py`  sebagaimana kebutuhan kita yang kita tulis diatas. Sebelumnya, mari kita buat test dulu. Buka `test.py` yang ada di folder `demo` diatas.
> Hanya buat test untuk apa yang telah kita buat atau edit dari fungsi fungsi default django. Misal, kita meng-*override* `save` maka, kita test untuk itu saja. ***Begitu katanya***

```python
from django.test import TestCase
from .models import Kelas

class KelasModelTest(TestCase):
	def test_can_save_and_retrieve_kelas_item(self):
    	Kelas.objects.create(nama="Silat")
        kelas = Kelas.objects.all()
        self.assertEqual(len(kelas), 1)
        self.assertEqual(kelas[0].nama , "Silat")
```

- Kita jalankan testnya dengan `./manage.py test` dan akan dapatkan kesalahan. Tahu kenapa? Karena kita belum buat model kelasnya.,
- akhirnya, kita buat modelnya dahulu. Buka `models.py` dan ketikkan kode dibawah ini

```python
from django.db import models

class Kelas(models.Model):
    nama = models.CharField(max_length=100)

    def __str__(self):
        return self.nama
```
Kita jalankan testnya lagi. Ternyata kita masih dapatkan pesan error, intinya table tidak ditemukan. Maka kita butuh mengetikkan `./manage.py makemigrations` diterminal, dan jangan lupa menambahkan aplikasi kita di `settings.py`
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'demo', # <<--- Ini aplikasi kita
]
```
Test, akan passed.

Ok, satu lagi, kita akan membuat test buat `murid` tabel.
```python
class MuridModelTest(TestCase):
    def test_can_save_and_retrieve_murid_item(self):
        kelas = Kelas.objects.create(nama="Silat")
        murid = Murid.objects.create(
                                     kelas=kelas, 
                                     namadepan="sakkuun", 
                                     namabelakang="alaminiyah"
                                     )
        kelas = Kelas.objects.all()
        self.assertEqual(len(kelas), 1)
        self.assertEqual(len(kelas[0].murid.all()), 1)
        self.assertEqual(kelas[0].murid.all()[0].namadepan, 'sakkuun')
        self.assertEqual(kelas[0].murid.all()[0].namabelakang, 'alaminiyah')
```
dan jangan lupa meng-*import* `Murid` class di atas. Kita jalankan testnya lagi, maka kita akan mendapatkan error. Betul, karena kita belum buat Tablenya. 

Seperti diatas, berarti kebutuhan tabel kita spt berikut:
1. Mempunyai 2 field, `namadepan` dan `namabelakang`
2. Harus ada hubungan `ManyToOne` antara tabel `Murid` dengan `Kelas` yang akan kita definisikan menggunakan `ForeignKey` di `models.py` nanti.

Ok, kita tulis dahulu kodenya.
```python
#models.py
class Murid(models.Model):
    namadepan = models.CharField(max_length=100)
    namabelakang = models.CharField(max_length=100)
    kelas = models.ForeignKey(Kelas, related_name='murid')

    def __str__(self):
        return self.namadepan
```
Adapun `related_name` bila tidak kita definisikan disini, maka django secara otomatis memberikan nama "namamodel"_set sebagai `related_name`. Dan ini, kita gunakan sebagai nama untuk memanggil model `murid` lewat *parent*-nya sebagaimana yang telah kita lihat di `test.py`
### Membuat Form
Nah, saatnya kita membuat form. Berarti, karena model kita ada dua, kita butuh dua form. Pertama untuk menampung `kelas` dan yang kedua untuk menampung `murid`. Kali ini, kita akan membuat Menggunakan `formset_factory` secara manual, dan di pembahasan di akhir, kita akan ubah menggunakan `modelformset_factory` yang disediakan oleh django yang merupakan *shortcut*, dan tidak banyak beda dari orangtuanya -`formset_factory`- maksudnya.
```python
class KelasFormTest(TestCase):

    def form_data(self, nama):
        return KelasForm({'nama':nama})

    def test_valid_data(self):
        form = self.form_data(nama='sakkuun')
        self.assertTrue(form.is_valid())
```
Seperti biasa, test ini akan fail, karena kita belum menuliskan kodenya. Di test diatas, kita mengerti, bahwa kebuatuhan kita adalah membuat form dengan satu field bernama `nama` dengan type text. Dan valid dengan satu field tersebut. Kita buat file `forms.py` di folder `demo`
```python
#forms.py
from django import forms

class KelasForm(forms.Form):
    nama = forms.CharField(max_length=100)
```
Masih ada satu test lagi, yaitu dalam rangka untuk meyakinkan kita bahwa field `nama` itu dibutuhkan. Dan bila user tidak memasukkan `nama` maka, validasi akan memberikan nilai `False`.
```Python
#tests.py
def test_with_missing_nama_return_false_with_is_valid_method(self):
        form = self.form_data({})
        self.assertFalse(form.is_valid())
        error = form['nama'].errors.as_data()
        self.assertEqual(len(error), 1)
        self.assertEqual(error[0].code, 'required' )
```
> `error[0].code` kita dapatkan dari `ValidateError("pesan error", code="kode")`. 

Dan kode kita akan lulus pengujian.

Kita buat Pengujian satu lagi untuk `MuridForm`, yang spesifikasinya sbg berikut. 
1. Memiliki 2 field `namadepan` dan `namabelakang`
2. Kedua field tersebut harus di isi, tidak boleh kosong. Bila Kosong, maka validasi akan mengembalikan boolean `False`

```python
#tests.py
from .forms import MuridForm

class MuridFormTest(TestCase):


    def form_data(self, namadepan, namabelakang):
        return MuridForm({
                         'namadepan': namadepan,
                         'namabelakang': namabelakang
                         })

    def test_valid_data(self):
        form = self.form_data('sakkuun', 'alaminiyah')
        self.assertTrue(form.is_valid())

    def test_with_missing_namadepan_return_false_with_is_valid_method(self):
        form = self.form_data('', 'alaminiyah')
        self.assertFalse(form.is_valid())
        errors = form['namadepan'].errors.as_data()
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, 'required')

    def test_with_missing_nama_belakang_return_false_with_is_valid_method(self):
        form = self.form_data('sakkuun', '')
        self.assertFalse(form.is_valid())
        errors = form['namabelakang'].errors.as_data()
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, 'required')
```

Untuk penjelasan, tidak banyak berbeda dengan yang `KelasForm`, ada yang bingung? Anda dapat membaca penjelasannya diatas.

```python
#forms.py
class MuridForm(forms.Form):
    namadepan = forms.CharField(max_length=100)
    namabelakang = forms.CharField(max_length=100)
```
### Membuat Formset
Sebagaimana diatas, kita akan membuat formset dengan `formset_factory`. Dengan ketentuan:
1. Tidak boleh ada pengulangan data. Harus unik per input.
2. Bila ada pengulangan, maka fungsi `is_valid` akan mengembalikan nilai `False` dan akan mengembalikan kode `duplikat` dengan pesan `Nama depan atau nama belakang terduplikasi`

```python
#tests.py
from .forms import MuridFormSet


class MuridFormSetTest(TestCase):


    def form_data(self, 
                  namadepan, 
                  namabelakang, 
                  namadepan_2 = '', 
                  namabelakang_2=''):
        return MuridFormSet({
                            'form-TOTAL_FORMS':2,
                            'form-INITIAL_FORMS':0,
                            'form-MAX_NUM_FORMS':'',
                            'form-0-namadepan': namadepan,
                            'form-0-namabelakang': namabelakang,
                            'form-1-namadepan': namadepan_2,
                            'form-1-namabelakang': namabelakang_2,
                            })

    def test_with_valid_data(self):
        form = self.form_data('sakkuun', 'alaminiyah')
        self.assertTrue(form.is_valid())


```
- [ ] TODO: Menjelaskan tenngan management formset

Dan taraaa, aplikasi kita tidak lulus uji. Tulis dahulu kodenya.
```python
MuridFormSet = forms.formset_factory(MuridForm)
```
> Untuk formset, ketika kita tidak isi form kita, maka tetap dihitung valid. Mari kita coba.

```python
	def test_with_empty_data_also_return_true(self):
        form = self.form_data('', '')
        self.assertTrue(form.is_valid())
```

Adapun bila kita uji dengan salah satu form kita isi, dan yang lainnya tidak, maka akan mengembalikan nilai `False` saat validasi sebagaimana form diatas.
```python
	def test_withempty_nama_belakang_or_namadepan_return_false_during_validation(self):
        form = self.form_data('sakkuun', '')
        self.assertFalse(form.is_valid())
        form = self.form_data('', 'alaminiyah')
        self.assertFalse(form.is_valid())
```
Kecuali, bila kita telah set salah satu field dengan `not required`.
> Dalam prakteknya jangan test dua logic di satu fungsi, ini akan mempersulit debugging kita, atau kalau tidak tambah susah, maka akan memperlambat.

#### Validasi formset dengan `BaseFormSet`
Untuk, kebutuhan kita diatas, kita bisa dengan mendefinisikannya dengan menuliskannya di method `clean` yang ada di class`BaseFomSet`. Sebelum lebih lanjut, kita tuliskan testnya dahulu.
```python
#tests.py

	def test_with_duplicate_namadepan_return_false_during_validation(self):
        form = self.form_data(
                              namadepan='sakkuun', 
                              namabelakang='alaminiyah', 
                              namadepan_2='sakkuun', 
                              namabelakang_2='ihfazhillah')
        self.assertFalse(form.is_valid())
        self.assertEqual(form.non_form_errors().as_data()[0].code, 'duplikat')
```
Kita lihat kode diatas, kita tuliskan `namadepan_2` identik dengan `namadepan`. Maka, `is_valid` akan mengembalikan nilai `False`.
Di kode diatas juga kita melihat ada method `non_form_errors()`. Bila kita memanggil atribut `.errors` maka kita tidak akan mendapatkan pesan apa apa. Unuk memastikannya bisa dengan menuliskan `print(form.erros)` dengan menambahkannya di kode diatas.
```python
class BaseMuridFormSet(forms.formsets.BaseFormSet):


    def clean(self):
        
        if any(self.errors):
            return

        namadepans = []
        namabelakangs = []
        duplikat = False

        for form in self.forms:
            if form.cleaned_data:
                namadepan = form.cleaned_data['namadepan']

                if namadepan:
                    if namadepan in namadepans:
                        duplikat = True
                    namadepans.append(namadepan) #ingat, namadepan untuk satu objek, 
                                                                             # namadepans untuk list

                if duplikat:
                    raise forms.ValidationError("Nama depan atau belakang terduplikasi",
                                                code="duplikat")
```
Yup, sekarang kita uji `namabelakang` juga tidak boleh terduplikasi, kalau terduplikasi maka akan ada pesan dengan kode `duplikat`.

```python
	def test_with_duplicate_namadepan_return_false_during_validation(self):
        form = self.form_data(
                              namadepan='sakkuun', 
                              namabelakang='alaminiyah', 
                              namadepan_2='hubaibah', 
                              namabelakang_2='alaminiyah')
        self.assertFalse(form.is_valid())
        self.assertEqual(form.non_form_errors().as_data()[0].code, 'duplikat')
```
> Untuk prakteknya, seharusnya nama itu boleh sama. Iya kan?? Untuk demo saja ini.. 

Kode dibawah adalah kode dari `BaseMuridFormSet` lengkap.
```python
#forms.py
class BaseMuridFormSet(forms.formsets.BaseFormSet):


    def clean(self):
        
        if any(self.errors):
            return

        namadepans = []
        namabelakangs = []
        duplikat = False

        for form in self.forms:
            if form.cleaned_data:
                namadepan = form.cleaned_data['namadepan']
                namabelakang = form.cleaned_data['namabelakang']

                if namadepan:
                    if namadepan in namadepans:
                        duplikat = True
                    namadepans.append(namadepan) #ingat, namadepan untuk satu objek, 
                                                                             # namadepans untuk list
                if namabelakang:
                    if namabelakang in namabelakangs:
                        duplikat = True
                    namabelakangs.append(namabelakang)

                if duplikat:
                    raise forms.ValidationError("Nama depan atau belakang terduplikasi",
                                                code="duplikat")

```


### Views
Yap, sekarang kita aplikasikan formset kita ke views. Di `views.py` kita akan membuat beberapa fungsi:
- Untuk menampilkan semua kelas
- Untuk membuat kelas baru
- Untuk menampilkan detail satu kelas
- Untuk mengedit satu kelas

#### Menampilkan semua kelas
```python
#tests.py
from django.core.urlresolvers import reverse


class ViewTest(TestCase):


    def setUp(self):
        self.kelas = Kelas.objects.create(nama="nahwu")

    def test_tampilkan_list(self):
        response = self.client.get(reverse('semua_kelas'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'demo/index.html')
        self.assertContains(response, 'nahwu')
```
`reverse(string)` ada fungsi yang digunakan untuk mendapatkan absolute url dengan menggunakan nama urlnya.

Dan, ditest di atas, kita akan menguji beberapa hal:
- Url ditemukan
- template yang dipakai adalah 'demo/index.html'
- dan, kita bisa melihat kelas 'nahwu'.

Ketika kita menjalankan kode diatas, kita akan mendapatkan error yang berbunyi `django.core.urlresolvers.NoReverseMatch: Reverse for 'semua_kelas' with arguments '()' and keyword arguments '{}' not found. 0 pattern(s) tried: []
` yang berarti *django tidak dapat menemukan url yang bernama 'semua_kelas*. Jadi, kita harus mendefinisikannya dahulu di file `urls.py` didalam folder `demo` dan meng-*include* kan `demo/urls.py` ini kedalam `urls.py` yang ada di project kita.

Tambahkan ini ke `formset_demo/urls.py`. dan jangan lupa mengimport `django.conf.urls.include`.

```python

 url(r'^demo/', include('demo.urls'))
```

Adapun di `demo/urls.py`
```python
from django.conf.urls import url

urlpatterns = [url(r'^/$', views.index , name='semua_kelas'),
              ]
```
Yap, kita membuat url baru kita dengan fungsi `url(rute, view, nama)`. `rute` adalah berisi ekspresi regex digunakan untuk merutekan view kita. `view` adalah fungsi yang akan memproses data yang akan kita keluarkan. `nama` adalah string yang kita gunakan untuk me-*reverse* tadi.

Kita jalankan test, ternyata masih error. Karena kita belum menulis fungsi viewnya.

Untuk melulus ujikan test kita kali ini, ada beberapa langkah yang harus kita lakukan setelah mengatur `urls.py`:
1. Membuat fungsi index di `views.py`
2. Melakukan query untuk mengambil semua `Kelas` data
3. Mengembalikan query tersebut dengan fungsi `render` yang kita dapatkan dari `django.shorcuts`
4. Mendefinisikan template yaitu `demo/templates.py` di folder `demo/templates`
5. membuat file `index.html` di folder tersebut, dan menampilkan data dengan bahasa yang telah ditentukan oleh django templates.

Ok, langkah satu sampai 4, kita tulis di satu script.
```python
from django.shorcuts import render
from .models import Kelas


def index(request):
	kelas = Kelas.objects.all()
    return render(request, "demo/index.html", 
    {'kelas_kelas':kelas})
```
Dan di `index.html`:
```django
<ul>
    {% for kelas in kelas_kelas %}
<td>
    {{ kelas }}
</td>
    {% endfor %}
</ul>
```

Di template django, `{% %}` digunakan untuk ekspresi, ekspresi pengulanagan, atau kondisional misalnya. sedankan `{{ }}` digunakan untuk variable, baik yang kita masukkan ke context melalui `views.py` atau yang kita definisikan di template itu sendiri.
#### Membuat Kelas Baru
Nah, di sini, kita akan mengaplikasikan form serta formset kita. Dengan tanpa data awalan. Adapun langkah secara garis besar adalah:
1. Mengecek apakah `request.method` adalah `POST` atau `GET`. 
2. Kalau `GET` maka tampilkan form kosong.
3. Kalau `POST` maka, proses data kita untuk kita masukkan kedatabase. Beserta validasinya.

##### `request.GET` method
Sekarang, kita akan memulai dengan method `GET` yang akan menampilkan form kosongan. Ok, mulai dengan testnya.

```python
    def test_get_create_url_return_200_and_form(self):
        response = self.client.get(reverse('create_kelas'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'demo/create_kelas.html')
        self.assertContains(response, 'form-MAX_NUM')
```
pertama, kita meng-get url, dan mencocokkan, bahwa django mendapatkan url dan url valid. Kemudian, mencocokkan bahwa template yang dipakai adalah `demo/create.html`. Dan memastikan bahwa `'form-MAX_NUM'` ada di template. `'form-MAX_NUM'` ini adalah formset management.

Minimal kode yang lulus test diatas adalah:
```python
def create(request):
    kelas_form = KelasForm()
    murid_form_set = MuridFormSet()
    return render(request, 'demo/create_kelas.html',
                  {'kelas_form':kelas_form,
                  'murid_form':murid_form_set})

```
Kita menginisiasi `kelas_form` yang berisi `KelasForm` yang sudah kita buat dengan data kosong. Dan menginisiasi `murid_form_set` dengan `MuridFormSet` yang sudah kita buat juga di `forms.py` Dan kita tampilkan di page.

Dan jangan lupa untuk men-append url dengan 
```python
url(r'^create/$', views.create, name='create_kelas'),
```
##### `request.POST` Method
Karena secara default fungsi kalau kita buat tanpa ekspresi kondisional akan memproses `GET` method, maka kita tidak perlu membuat `if else`. Namun, kalau kita ingin memproses `POST`, atau `PUT` atau `DELETE` atau yang lainnya, maka kita butuh ekspresi kondisional.
```python
#test.py
    def test_post_create_new_kelas_and_update_database(self):
        data = self.form_data("shorof", 
                              "sakkuun", 
                              "alaminiyah")
        response = self.client.post(reverse('create_kelas'), data=data)
        kelas = Kelas.objects.all()
        kelas_nahwu = kelas[0]
        kelas_shorof = kelas[1]
        self.assertEqual(len(kelas), 2)
        self.assertEqual(kelas_nahwu.nama, 'nahwu')
        self.assertEqual(kelas_shorof.nama, 'shorof')
        self.assertEqual(kelas_shorof.murid.first().namadepan, 'sakkuun')
        self.assertRedirects(response, reverse('semua_kelas'))
```
Di test diatas, kita akan menguji apakah database terupdate atau tidak dengan post request yang kita pinta, dan apakah url teralihkan setelah selesai operasi?

Kita langsung fokus ke `views.py` karena url yang dipakai sama dengan yang diatas. Ada sedikit perubahan kode yang diatas, yakni di get request. Dengan memasukkan kode diatas ke kondisi `request.method == 'GET'` dan menambahkan kondisi `request.method == 'POST'` dan menuliskan kode baru kita di bawahnya.
Untuk langkah yang kita lakukan adalah :
1. Membuat form menggunakan `KelasForm` dengan isi data dari `request.POST`, dan juga `MuridFormSet`
2. Memastikan form telah valid, kemudian...
3. Memastikan, bahwa form sudah terisi.
4. Mengambil nama `kelas` dan kita save kedalam database
5. Membuat perulangan untuk mengambil form murid satu persatu, 
6. dari setiap form, kita ambil `namadepan` dan `namabelakang`
7. save murid kedalam kelas yang sesuai
8. redirect ke halaman utama

adapun kodenya:

```python
#views.py

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import models
from .forms import KelasFOrm, MuridFormSet


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

```
Dan pastikan, aplikasi kita sudah lulus uji.

#### Menampilkan Detail Suatu Kelas
Oke, saatnya kita ingin menampilkan data yang telah kita buat.
```python
#tests.py

    def test_get_first_data_and_render_in_page(self):
        self.kelas.murid.create(namadepan='sakkuun',
                                namabelakang='alaminiyah')
        response = self.client.get(reverse('kelas_detail', args=[self.kelas.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['kelas'].nama, 'nahwu')
        self.assertEqual(response.context['murids'][0].namadepan, 'sakkuun')
        self.assertEqual(response.context['murids'][0].namabelakang, 'alaminiyah')
        self.assertTemplateUsed(response, 'demo/kelas_detail.html')
        self.assertContains(response, 'nahwu')
```
Di pengujian ini, kita akan menguji apakah nama kelas, dan murid bisa di dapatkan di halaman detail atau tidak? Setidaknya, kita bisa menambahkannya kelak di template meskipun kita belum menulis apa apa di template. Dan menguji apakah template yang digunakan benar benar `demo/kelas_detail.html` atau tidak. 
Perhatikan method `reverse`, kita memasukkan `args` sebagai parameter. `args` adalah list dari argument yang akan kita masukkan ke url. Disini, kita memasukkan id kelas sebagai parameter url. Dalam prakteknya, kita gak harus pakai id, bisa pakai yang lainnya misal menggunakan slug.

Dan pasti, anda akan mendapatkan pesan, url tidak ditemukan dikarenakan belum membuat menambahkan urlpatternnya.
```python
url(r'^(?P<pk>\d+)/$', views.detail, name='kelas_detail'),
```
Pattern diatas, kalau misalkan id adalah 1, maka url akan menjadi `/demo/1`. Dan akan memasukkan parameter `pk` kedalam view. 
```python
def detail(request, pk):
    kelas = Kelas.objects.get(pk=pk)
    murids = kelas.murid.all()
    return render(request, 'demo/kelas_detail.html',
                  {'kelas':kelas,
                  'murids':murids})
```
Syuf, ujian program kita lulus.
##### Bagaimana kalau url tidak ditemukan?
Yuk, kita test dahulu. Seharusnya kalau benar, `status_code` nya akan menjadi `404` dan tidak ada pesan lain selain itu.
```python
    def test_detail_data_with_nonexist_data(self):
        response = self.client.get(reverse('kelas_detail', args=[10]))
        self.assertEqual(response.status_code, 404)
```
Jalankan test, oh, ternyata...
```python
demo.models.DoesNotExist: Kelas matching query does not exist.
```
ini pesan yang kita dapatkan. Untuk itu, kita perlu menyembunyikan pesan ini, dan hanya mendapatkan halaman 404 Not Found.

Kita edit sedikit viewnya, import `get_object_or_404` dari `django.shortcuts` dan ubah
```python
kelas = Kelas.objects.get(pk=pk)
```
menjadi:
```python
kelas = get_object_or_404(Kelas, pk=pk)
```
jalankan uji coba, dan anda kan mendapatkan pesan LOLOS.

#### Edit Detail
Tidak banyak perubahan dengan Point Kedua diatas, kita perlu mengecek, requestnya apa. Kalau `GET` Maka **tampilkan data yang ada** kalau `POST` maka **Edit database yang ada**.
##### POST
```python
#tests.py

	    def test_edit_first_kelas(self):
        data = self.form_data(namakelas='shorof', 
                              namadepan='ihfazh', 
                              namabelakang='alaminiy', 
                              namadepan_2='sakkuun', 
                              namabelakang_2='alaminiyah')
        response = self.client.post(reverse('edit_kelas', args=[self.kelas.id]), 
                                    data=data)
        self.assertRedirects(response, reverse('kelas_detail', args=[self.kelas.id]))
        kelas = Kelas.objects.get(id=self.kelas.id)
        self.assertEqual(kelas.nama, 'shorof')
        self.assertEqual(len(kelas.murid.all()), 2)
        self.assertEqual(kelas.murid.first().namadepan, 'ihfazh')
        self.assertEqual(kelas.murid.first().namabelakang, 'alaminiy')
```
pastikan, data terubah, dan teredirect ke halaman detail. Jangan lupa buat url patternya dahulu.
```python
url(r'^(?P<pk>\d+)/edit/$', views.edit, name='edit_kelas'),
```
dan viewnya
```python
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

            for index, muridform in enumerate(murid_form):
                
                nama_depan = muridform.cleaned_data['namadepan']
                nama_belakang = muridform.cleaned_data['namabelakang']
                murid , created = Murid.objects.get_or_create(id=index, kelas=kelas)

                
                murid.namadepan = nama_depan
                murid.namabelakang = nama_belakang
                murid.save()
			return redirect(reverse('kelas_detail', args=[kelas.pk]))
```
Tidak banyak berubah, kecuali karena kita ingin merubah maka di setelah validasi sedikit berbeda. Terutama untuk mengesave field murid.
Jadi, karena setiap murid yang paling unik adalah id, yang tidak bisa kita dapatkan dari inputan user, maka kita ambil menggunakan fungsi bawaan python yang berupa `enumerate` yang akan mengembalikan tuple berupa index, dan value. Index ini saya gunakan untuk `id`.
Nah, `get_or_create` ini artinya kalau kamu bisa ambil ambil, kalau tidak, maka buat baru. Dan mengembalikan tuple berupa objek, dan boolean yang bernilai `True` atau `False`. Jadi, misalkan `id=0` maka, dapatkan objek dengan id yang bernilai nol. Dapat? Kalau tidak, maka buat objek -disini murid- baru dengan id bernilai nol.
##### GET
```python
def test_edit_detail_wit_get_request(self):
        Murid.objects.create(kelas=self.kelas, 
                             namadepan='namadepan', 
                             namabelakang='namabelakang')
        response = self.client.post(reverse('edit_kelas', args=[self.kelas.id]))
        self.assertContains(response, 'nahwu')
        self.assertContains(response, 'namadepan')
        self.assertContains(response, 'namabelakang')
        self.assertTrue(response.context['kelas_form'])
        self.assertTrue(response.context['murid_form'])
        self.assertTemplateUsed(response, 'demo/edit_kelas.html')
```
Penjelasan tidak banyak beda dengan create_kelas. Bisa ditengok keatas.
Adapun pengecekan 'nahwu', 'namadepan', 'namabelakang' adalah mengecek initial datanya, betul atau tidak.
dan `assertTrue` dibawah `assertTemplate` adalah untuk mengecek, apakah kedua context sudah ada atau belum.

```python
#views.py lengkap dengan post request
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

            for index, muridform in enumerate(murid_form):
                
                nama_depan = muridform.cleaned_data['namadepan']
                nama_belakang = muridform.cleaned_data['namabelakang']
                murid , created = Murid.objects.get_or_create(id=index, kelas=kelas)

                
                murid.namadepan = nama_depan
                murid.namabelakang = nama_belakang
                murid.save()

            return redirect(reverse('kelas_detail', args=[kelas.pk]))
    kelas_form = KelasForm(initial=initial_kelas)
    murid_form = MuridFormSet(initial=initial_murid)
    return render(request, 'demo/edit_kelas.html',
                  {'kelas_form':kelas_form,
                  'murid_form':murid_form})
```

### Memecah test class ke beberapa file
Buat folder baru di dalam folder `demo` bernama `tests` dan buat file kosong baru bernama 
`__init__.py` untuk memberitahu kepada `python` bahwa folder `tests` adalah modul.
Kemudian, *copykan* file `tests.py` kedalam folder ini. Dan buat tiga file baru. Seperti pohon folder
dibawah ini 
```
demo/tests
├── __init__.py
├── test_forms.py
├── test_models.py
└── test_views.py
```

Sebagaimana anda lihat, file `tests.py` sudah tidak ada diatas. Karena sudah saya pindah pindah. 
Anda bisa melihatnya di repository. Yang intinya, saya pindah sesuai __"Kita lagi test apa?"__
#### TODO
- [ ] Menggunakan `modelformset_factory` dan `ModelForm` agar tidak mengulang ulang penulisan di `forms.py`. Karena kita lihat, bahwa form yang kita buat di `forms.py` identik dengan field yang ada di `models.py`