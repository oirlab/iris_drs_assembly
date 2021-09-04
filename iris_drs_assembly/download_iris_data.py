import urllib.request
import zipfile
import os.path

if not os.path.exists("iris_example_data/raw_flat_frame_cal.fits"):
    urllib.request.urlretrieve(
        "https://ndownloader.figshare.com/articles/9941939/versions/1",
        "iris_example_data.zip"
    )

    with zipfile.ZipFile("iris_example_data.zip", 'r') as zip_ref:
        zip_ref.extractall("iris_example_data")
