import json

import route_guide_pb2


def read_route_guide_database():
    """Reads the route guide database.

    Returns:
      The full contents of the route guide database as a sequence of
        route_guide_pb2.Features.
    """
    feature_list = []
    with open("route_guide_db.json") as route_guide_db_file:
        for item in json.load(route_guide_db_file):
            feature = route_guide_pb2.Feature(
                number=route_guide_pb2.Point(
                    number=item["number"]
                )
            )
            feature_list.append(feature)
    return feature_list
