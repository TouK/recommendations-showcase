# Recommendations showcase notebook

[Jupyter notebook](/model-training/recommendations_model_training.ipynb) presenting the lifecycle of a ML model for the recommendations scenario example.

## Local setup

Note that the local setup has some [limitations](#model-deployment-phrasing) related to model deployment.

Easiest way to get started is by using the Anaconda distribution.

1. Create and activate a new conda environment with Python 3.10
```shell
$ conda create -n <environment_name> python=3.10
$ conda activate <environment_name>
```
2. Install dependencies
```shell
$ pip install -r requirements.txt
```
3. Run Jupyter Notebook
```shell
jupyter notebook
```
and open the [recommendations showcase notebook](sli_rec_on_custom_dataset_on_databricks.ipynb).

### Model deployment

The Databricks deployment step won't work locally due to the fact that the notebook is assumed to be executed
from within the Databricks environment. To log the model from outside the Databricks environment, configure the
Databricks registry url, credentials and experiment name by executing the following code before logging the model:

```python
os.environ["DATABRICKS_HOST"] = "<INSERT_DATABRICKS_URL_HERE>"
os.environ["DATABRICKS_CLIENT_ID"] = "<INSERT_CLIENT_ID_HERE>"
os.environ["DATABRICKS_CLIENT_SECRET"] = "<INSERT_CLIENT_SECRET_HERE>"

mlflow.set_registry_uri("databricks")
mlflow.set_tracking_uri("databricks")

# This is the experiment name in Databricks specific format
EXPERIMENT_NAME = "/Users/<INSERT_USERNAME_HERE>/<INSERT_EXPERIMENT_NAME_HERE>"
mlflow.set_experiment(EXPERIMENT_NAME)
```
