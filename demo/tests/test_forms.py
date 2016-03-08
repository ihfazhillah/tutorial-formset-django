from django.test import TestCase
from ..forms import KelasForm, MuridForm, MuridFormSet


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

    def test_with_duplicate_namabelakang_return_false_during_validation(self):
        form = self.form_data(
                              namadepan='sakkuun', 
                              namabelakang='alaminiyah', 
                              namadepan_2='hubaibah', 
                              namabelakang_2='alaminiyah')
        self.assertFalse(form.is_valid())
        self.assertEqual(form.non_form_errors().as_data()[0].code, 'duplikat')
