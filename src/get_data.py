import zipfile

import requests


def download_data_from_kaggle():
    dataset_url = "https://bit.ly/3phWvY1"
    dataset = requests.get(dataset_url)
    with open("./data/dataset.zip", "wb") as output_file:
        output_file.write(dataset.content)


# def unzip_downloaded_data():
#    with zipfile.ZipFile('./data/dataset.zip', 'r') as zip_ref:
#        zip_ref.extractall("./data")


if __name__ == "__main__":
    download_data_from_kaggle()
    # unzip_downloaded_data()
