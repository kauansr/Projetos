from django.test import TestCase
from django.urls import reverse


class TestedeViews(TestCase):

    def test_se_login_retorna_status_code_200(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)

    
    def test_se_login_retorna_template_usado_certo(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'perfil/login.html')
    

    
    def test_se_cadastro_retorna_status_code_200(self):
        response = self.client.get(reverse('cadastro'))
        self.assertEquals(response.status_code, 200)

    
    def test_se_cadastro_retorna_template_usado_certo(self):
        response = self.client.get(reverse('cadastro'))
        self.assertTemplateUsed(response, 'perfil/cadastro.html')
    
    def test_se_atualizar_retorna_status_code_200(self):
        response = self.client.get(reverse('atualizar'))
        self.assertNotEqual(response.status_code, 200)

    
    def test_se_atualizar_retorna_template_usado_certo(self):
        response = self.client.get(reverse('atualizar'))
        self.assertTemplateNotUsed(response, 'perfil/atualizar.html')
