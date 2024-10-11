from concurrent import futures
import logging
import time
import grpc
import multiplication_pb2
import multiplication_pb2_grpc
import multiplication_resources


def get_multiplier(feature_db, point):
    """Returns Feature at given number or None."""
    for feature in feature_db:
        if feature.number == point:
            return feature
    return None


def get_number(get):
    """Getting number"""
    current_number = get.number
    return current_number


class MultiplicationServicer(multiplication_pb2_grpc.MultiplicationServicer):
    """Provides methods that implement functionality of multiplication server."""

    def __init__(self):
        self.db = multiplication_resources.read_multiplication_database()

    def GetMultiplier(self, request, context):
        feature = get_multiplier(self.db, request)
        if feature is None:
            return multiplication_pb2.Multiplier(number=request)
        else:
            return feature

    def ListMultipliers(self, request, context):
        least = min(request.lo.number, request.hi.number)
        most = max(request.lo.number, request.hi.number)
        for feature in self.db:
            if (
                    feature.number.number >= least
                    and feature.number.number <= most
            ):
                yield feature

    def RecordMultiplication(self, request_iterator, context):
        point_count = 0
        feature_count = 0
        multiplication_result = 1

        start_time = time.time()
        for point in request_iterator:
            point_count += 1
            if get_multiplier(self.db, point):
                feature_count += 1
                multiplication_result *= get_number(point)

        elapsed_time = time.time() - start_time
        return multiplication_pb2.MultiplicationSummary(
            point_count=point_count,
            feature_count=feature_count,
            multiplication_result=multiplication_result,
            elapsed_time=int(elapsed_time),
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    multiplication_pb2_grpc.add_MultiplicationServicer_to_server(
        MultiplicationServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
