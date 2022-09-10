import zipfile


def unzip_downloaded_data(target_data_path):
    """Unzip the dataset inside the data folder"""
    with zipfile.ZipFile("./data/dataset.zip", "r") as zip_ref:
        # zip_ref.extractall("./data")
        zip_ref.extractall(target_data_path)


if __name__ == "__main__":
    unzip_downloaded_data("./data")
    # unzip_downloaded_data("./monitoring_service/evidently_service/datasets")
