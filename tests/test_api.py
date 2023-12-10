import time
from urllib.parse import quote


def test_get_data_in_disk(api_client):
    response = api_client.get()
    assert response.status_code == 200
    # print(json.dumps(response.json(), indent=2)) # Для вывода информации в JSON


def test_create_folder(api_client):
    folder_path = 'Test Folder'
    api_client.create_folder(folder_path)


def test_get_info_created_folder(api_client):
    folder = 'Test Folder'
    encoded_path = quote(folder)
    response = api_client.get(f'resources?path={encoded_path}')
    assert response.status_code == 200


def test_upload_file_into_folder(api_client):
    remote_folder_path = "/Test Folder"
    local_file_name = '/TokenYandex.txt'
    remote_file_path = f"{remote_folder_path}{local_file_name}"

    local_file_path = "C:\\Users\\illya\\OneDrive\\Рабочий стол\\TokenYandex.txt"
    response = api_client.upload_file(local_file_path, remote_file_path, 'resources/upload', overwrite=True)
    assert response.status_code == 201


def test_put_item_in_cart(api_client):
    disk_folder_path = '/Test Folder'
    api_client.delete_item(disk_folder_path)


def test_create_my_photo_folder(api_client):
    folder_path = 'My Photo'
    api_client.create_folder(folder_path)


def test_download_file_from_inet(api_client):
    download_url = "https://gas-kvas.com/uploads/posts/2023-02/1675474058_gas-kvas-com-p-fonovii-risunok-rabochego-stola-peizazh-32.jpg"
    remote_folder_path = "/My Photo"
    name_of_file = "/Photo"

    api_client.post('resources/upload', download_url, remote_folder_path + name_of_file)
    time.sleep(5)


def test_put_file_from_folder_in_cart(api_client):
    disk_folder_path = '/My Photo/Photo'
    api_client.delete_item(disk_folder_path)


def test_clean_cart(api_client):
    api_client.clean_trash()
