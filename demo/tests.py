from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Kelas, Murid
from .forms import KelasForm, MuridForm, MuridFormSet

class KelasModelTest(TestCase):
    def test_can_save_and_retrieve_kelas_item(self):
        Kelas.objects.create(nama="Silat")
        kelas = Kelas.objects.all()
        self.assertEqual(len(kelas), 1)
        self.assertEqual(kelas[0].nama , "Silat")

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

class KelasFormTest(TestCase):

    def form_data(self, nama):
        return KelasForm({'nama':nama})

    def test_valid_data(self):
        form = self.form_data(nama='sakkuun')
        self.assertTrue(form.is_valid())

    def test_with_missing_nama_return_false_with_is_valid_method(self):
        form = self.form_data({})
        self.assertFalse(form.is_valid())
        error = form['nama'].errors.as_data()
        self.assertEqual(len(error), 1)
        self.assertEqual(error[0].code, 'required' )

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

    def test_with_empty_data_also_return_true(self):
        form = self.form_data('', '')
        self.assertTrue(form.is_valid())

    def test_withempty_nama_belakang_or_namadepan_return_false_during_validation(self):
        form = self.form_data('sakkuun', '')
        self.assertFalse(form.is_valid())
        form = self.form_data('', 'alaminiyah')
        self.assertFalse(form.is_valid())

    def test_with_duplicate_namadepan_return_false_during_validation(self):
        form = self.form_data(
                              namadepan='sakkuun', 
                              namabelakang='alaminiyah', 
                              namadepan_2='sakkuun', 
                              namabelakang_2='ihfazhillah')
        self.assertFalse(form.is_valid())
        self.assertEqual(form.non_form_errors().as_data()[0].code, 'duplikat')

    def test_with_duplicate_namadepan_return_false_during_validation(self):
        form = self.form_data(
                              namadepan='sakkuun', 
                              namabelakang='alaminiyah', 
                              namadepan_2='hubaibah', 
                              namabelakang_2='alaminiyah')
        self.assertFalse(form.is_valid())
        self.assertEqual(form.non_form_errors().as_data()[0].code, 'duplikat')

class ViewTest(TestCase):

    def form_data(self, 
                  namakelas ,
                  namadepan, 
                  namabelakang, 
                  namadepan_2 = '', 
                  namabelakang_2=''):
        return {       'nama':namakelas,
                            'form-TOTAL_FORMS':2,
                            'form-INITIAL_FORMS':0,
                            'form-MAX_NUM_FORMS':'',
                            'form-0-namadepan': namadepan,
                            'form-0-namabelakang': namabelakang,
                            'form-1-namadepan': namadepan_2,
                            'form-1-namabelakang': namabelakang_2,
                            }

    def setUp(self):
        self.kelas = Kelas.objects.create(nama="nahwu")

    def test_tampilkan_list(self):
        response = self.client.get(reverse('semua_kelas'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'demo/index.html')
        self.assertContains(response, 'nahwu')

    def test_get_create_url_return_200_and_form(self):
        response = self.client.get(reverse('create_kelas'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'demo/create_kelas.html')
        self.assertContains(response, 'form-MAX_NUM')

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

    def test_detail_data_with_nonexist_data(self):
        response = self.client.get(reverse('kelas_detail', args=[10]))
        self.assertEqual(response.status_code, 404)

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
        #editing must not create new
        kelases = Kelas.objects.all()
        self.assertEqual(len(kelases), 1)

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

