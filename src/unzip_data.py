import zipfile


def unzip_downloaded_data():
    with zipfile.ZipFile("./data/dataset.zip", "r") as zip_ref:
        zip_ref.extractall("./data")


if __name__ == "__main__":
    unzip_downloaded_data()
