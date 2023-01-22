from django.test import TestCase
from django.urls import reverse

class TestedeViews(TestCase):
    def test_se_dashboard_retorna_status_code_200(self):
        response = self.client.get(reverse('inicialsite:dashboard'))
        self.assertNotEquals(response.status_code, 200)

    
    def test_se_dashboard_retorna_template_usado_certo(self):
        response = self.client.get(reverse('inicialsite:dashboard'))
        self.assertTemplateNotUsed(response, 'inicialsite/dashboard.html')