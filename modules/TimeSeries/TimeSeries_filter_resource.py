from typing import List

from core.base_resource import BaseResource
from modules.TimeSeries.TimeSeries_model import TimeSeriesModel
from falcon import *
import json


class TimeSeriesFilterResource(BaseResource):
    """
    TimeSeries resource handler
    """
    model = TimeSeriesModel
    property_types = []
    allowed_methods = ["POST"]

    @falcon.after(BaseResource.conn.close)
    def on_post(self, req=None, resp=None):
        """
        Post mapping
        :param req: Object
        :param resp: Object
        :return:
        """
        req_body = req.stream.read().decode('utf-8')
        req_data = json.loads(req_body, encoding='utf-8')
        if "min" and "max" in req_data:

            min_val = req_data['min']
            max_val = req_data['max']

            data = self.model.select()\
                             .where(self.model.temperature.between(min_val, max_val))\
                             .order_by(self.model.temperature, self.model.time)
            resp.status = falcon.HTTP_200
            resp.content_type = "application/json"
            filtered_data = []

            if len(data) != 0:
                items: List[TimeSeriesModel] = []
                for item in data:
                    items.append(item.to_dict())
                filtered_data = items
            resp.body = (json.dumps(filtered_data, indent=4, sort_keys=True, default=str))

            return
        self.__bad_request__(resp, {
            "message": "missing min and max properties"
        })
