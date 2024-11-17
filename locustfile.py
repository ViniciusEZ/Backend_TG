from locust import HttpUser, task
from random import randint

class UserAccess(HttpUser):
    options = ['Mais vendidos', 'Preço decrescente', 'Preço crescente', 'default']

    search_options = ['RTX', 'AMD', 'INTEL']
    @task
    def create_new_user(self):
        self.client.get(
            f'/products/get-products?sort={self.options[randint(0, len(self.options)-1)]}',
        )

        # self.client.get(
        #     f'/products/search/{self.search_options[randint(0, len(self.search_options)-1)]}',
        # )