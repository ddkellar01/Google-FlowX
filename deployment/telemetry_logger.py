from google.cloud import monitoring_v3
import time

class TelemetryLogger:
    """Streams real-time pipeline metrics to Google Cloud Monitoring / Grafana dashboards."""
    
    def __init__(self, project_id: str):
        self.client = monitoring_v3.MetricServiceClient()
        self.project_name = f"projects/{project_id}"

    def log_pipeline_metric(self, metric_type: str, value: float):
        series = monitoring_v3.TimeSeries()
        series.metric.type = f"custom.googleapis.com/flowx/{metric_type}"
        
        point = monitoring_v3.Point()
        point.value.double_value = value
        now = time.time()
        point.interval.end_time.seconds = int(now)
        point.interval.end_time.nanos = int((now - point.interval.end_time.seconds) * 10**9)
        
        series.points = [point]
        self.client.create_time_series(name=self.project_name, time_series=[series])
        print(f"Telemetry logged: {metric_type} = {value}")
