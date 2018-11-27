from modules.TimeSeries.TimeSeries_resource import TimeSeriesResource
from modules.TimeSeries.TimeSeries_filter_resource import TimeSeriesFilterResource

routes = [
    # TimeSeries api routes
    {'url': '/v1/time-data', 'controller': TimeSeriesResource()},
    {'url': '/v1/time-data/{uid}', 'controller': TimeSeriesResource()},
    {'url': '/v1/time-data/filter', 'controller': TimeSeriesFilterResource()}
]
