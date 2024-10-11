from concurrent import futures
import logging
import time

import grpc
import route_guide_pb2
import route_guide_pb2_grpc
import route_guide_resources


def get_feature(feature_db, point):
    """Returns Feature at given number or None."""
    for feature in feature_db:
        if feature.number == point:
            return feature
    return None


def get_number(get):
    """Getting number"""
    current_number = get.number
    return current_number


class RouteGuideServicer(route_guide_pb2_grpc.RouteGuideServicer):
    """Provides methods that implement functionality of route guide server."""

    def __init__(self):
        self.db = route_guide_resources.read_route_guide_database()

    def GetFeature(self, request, context):
        feature = get_feature(self.db, request)
        if feature is None:
            return route_guide_pb2.Feature(number=request)
        else:
            return feature

    def ListFeatures(self, request, context):
        least = min(request.lo.number, request.hi.number)
        most = max(request.lo.number, request.hi.number)
        for feature in self.db:
            if (
                    feature.number.number >= least
                    and feature.number.number <= most
            ):
                yield feature

    def RecordRoute(self, request_iterator, context):
        point_count = 0
        feature_count = 0
        multiplication_result = 1

        start_time = time.time()
        for point in request_iterator:
            point_count += 1
            if get_feature(self.db, point):
                feature_count += 1
                multiplication_result *= get_number(point)

        elapsed_time = time.time() - start_time
        return route_guide_pb2.RouteSummary(
            point_count=point_count,
            feature_count=feature_count,
            multiplication_result=multiplication_result,
            elapsed_time=int(elapsed_time),
        )

    def RouteChat(self, request_iterator, context):
        prev_notes = []
        for new_note in request_iterator:
            for prev_note in prev_notes:
                if prev_note.number == new_note.number:
                    yield prev_note
            prev_notes.append(new_note)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    route_guide_pb2_grpc.add_RouteGuideServicer_to_server(
        RouteGuideServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
