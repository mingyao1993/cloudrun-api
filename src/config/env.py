import os


class ApplicationEnv:
    @property
    def project_id(self):
        return os.environ.get("PROJECT_ID")

    @property
    def datastore_namespace(self):
        return os.environ.get("DATASTORE_NAMESPACE")


app_config = ApplicationEnv()
