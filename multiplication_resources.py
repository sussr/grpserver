import json
import multiplication_pb2


def read_multiplication_database():
    """Reads the multiplication database.

    Returns:
      The full contents of the multiplication database as a sequence of
        multiplication_pb2.Features.
    """
    feature_list = []
    with open("multiplication_db.json") as multiplication_db_file:
        for item in json.load(multiplication_db_file):
            feature = multiplication_pb2.Multiplier(
                number=multiplication_pb2.Point(
                    number=item["number"]
                )
            )
            feature_list.append(feature)
    return feature_list
