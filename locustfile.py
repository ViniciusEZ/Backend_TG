from locust import HttpUser, task
from random import randint
from faker import Faker
from os import urandom

class UserAccess(HttpUser):
    options = ['Mais vendidos', 'Preço decrescente', 'Preço crescente', 'default']
    search_options = ['RTX', 'AMD', 'INTEL']
    fake = Faker()
    @task
    def create_new_user(self):
        self.client.get(
             f'/products/get-products?sort={self.options[randint(0, len(self.options)-1)]}',
        )

        self.client.get(
            f'/products/search/{self.search_options[randint(0, len(self.search_options)-1)]}',
        )

        with self.client.get(
            f'/products/product/{randint(1, 20)}',
        catch_response=True) as response:
            if response.status_code == 404:
                response.success()

        with self.client.post(
            '/user/register/',
            json={
                "email": self.fake.email(),
                "name": self.fake.name(),
                "phone_number": self.fake.phone_number(),
                "cpf": int.from_bytes(urandom(4)),
                "password": self.fake.password(length=12),
                "addresses": [
                        {
                            "cep": randint(10000000, 99999999),
                            "logradouro": self.fake.address(),
                            "numero": randint(1, 999),
                            "complemento": f"Casa {randint(1, 100)}",
                            "bairro": self.fake.city(),
                            "cidade": self.fake.city(),
                            "uf": self.fake.city()[:2]
                        }
                ]
            }
        , catch_response=True) as response:
            if response.status_code == 409:
                response.success()
