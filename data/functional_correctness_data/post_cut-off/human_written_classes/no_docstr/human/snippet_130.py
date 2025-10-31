class _MlflowLoggingAdapter:

    def log(self, data, step):
        import mlflow
        results = {k.replace('@', '_at_'): v for k, v in data.items()}
        mlflow.log_metrics(metrics=results, step=step)

    def finish(self):
        import mlflow
        mlflow.end_run()