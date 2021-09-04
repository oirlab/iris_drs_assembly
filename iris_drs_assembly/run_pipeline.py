import os

import iris_pipeline

iris_pipeline.monkeypatch_jwst_datamodels()

pipeline = iris_pipeline.pipeline.ProcessImagerL2Pipeline
pipeline.call("association.json", config_file="image2_iris.cfg")
