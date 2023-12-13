import requests
from urllib.parse import quote
import time
from config import BASE_URL


class APIClient:
    def __init__(self, oauth_token=None):
        # Используется значение по умолчанию None, чтобы API-клиент мог быть создан без токена
        self.base_url = BASE_URL
        self.headers = {"Authorization": f"OAuth {oauth_token}"} if oauth_token else {}

    def make_url(self, endpoint):
        return f"{self.base_url}{endpoint}"

    def get(self, endpoint=None):
        url = self.make_url(endpoint) if endpoint else self.base_url  # Проверка наличия Endpoint
        response = requests.get(url, headers=self.headers)
        return response

    def post(self, endpoint, download_url, name_of_file):
        upload_url = self.make_url(endpoint)
        params = {
            "url": download_url,
            "path": name_of_file,
        }
        response = requests.post(upload_url, headers=self.headers, params=params)
        return response

    def put(self, endpoint):
        url = self.make_url(endpoint)
        response = requests.put(url, headers=self.headers)
        return response

    def delete(self, endpoint):
        url = self.make_url(endpoint)
        response = requests.delete(url, headers=self.headers)
        return response

    def upload_file(self, file_path, remote_path, endpoint, overwrite):
        upload_url = self.make_url(endpoint)
        params = {
            "path": remote_path,
            "overwrite": str(overwrite).lower()
        }
        response = requests.get(upload_url, headers=self.headers, params=params)
        upload_info = response.json()

        if 'href' in upload_info:
            with open(file_path, 'rb') as file:
                files = {'file': file}
                upload_response = requests.put(upload_info['href'], files=files)
                return upload_response
        else:
            return response

    def create_folder(self, folder_path):
        check_resp = self.get(f'resources?path={quote(folder_path)}')
        if check_resp.status_code == 404:
            create_resp = self.put(f'resources?path={quote(folder_path)}')
            assert create_resp.status_code == 201
            time.sleep(5)

    def delete_item(self, item_path):
        encoded_item_path = quote(item_path)
        resp = self.delete(f'resources?path={encoded_item_path}')

        assert resp.status_code in (202, 204)
        if resp.status_code == 202:
            operation_id = resp.json().get('operation_id')
            if operation_id:
                time.sleep(5)
                check_resp = self.get(f'operations/{operation_id}')
                assert check_resp.status_code == 204

    def clean_trash(self):
        response = self.delete('trash/resources')

        assert response.status_code in (202, 204)
        if response.status_code == 202:
            operation_id = response.json().get('operation_id')
            if operation_id:
                time.sleep(5)
                check_response = self.get(f'operations/{operation_id}')
                assert check_response.status_code == 204
