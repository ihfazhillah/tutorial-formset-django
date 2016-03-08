from django.test import TestCase
from ..models import Kelas, Murid


class KelasModelTest(TestCase):
    def test_can_save_and_retrieve_kelas_item(self):
        Kelas.objects.create(nama="Silat")
        kelas = Kelas.objects.all()
        self.assertEqual(len(kelas), 1)
        self.assertEqual(kelas[0].nama, "Silat")


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