from django.test import TestCase
from django.core.urlresolvers import reverse
from ..models import Kelas, Murid


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

