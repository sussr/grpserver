from __future__ import print_function

import logging
import grpc
import multiplication_pb2
import multiplication_pb2_grpc
import multiplication_resources


def format_point(point):
    return "number: %d" % point.number


def guide_list_multipliers(stub):
    rectangle = multiplication_pb2.Rectangle(
        lo=multiplication_pb2.Point(number=1),
        hi=multiplication_pb2.Point(number=10),
    )
    print("Looking for numbers between 1 and 10")

    multipliers = stub.ListMultipliers(rectangle)
    for multiplier in multipliers:
        print(f"Found number: {format_point(multiplier.number)}")


def generate_route(feature_list, count):
    # Limit to `count` numbers from the feature list
    for i in range(min(count, len(feature_list))):
        feature = feature_list[i]
        print(f"Visiting point {format_point(feature.number)}")
        yield feature.number


def guide_record_multiplication(stub, count=10):
    feature_list = multiplication_resources.read_multiplication_database()
    route_iterator = generate_route(feature_list, count)
    route_summary = stub.RecordMultiplication(route_iterator)
    print(f"Passed {route_summary.feature_count} features")
    print(f"Multiplication result: {route_summary.multiplication_result}")
    print(f"It took {route_summary.elapsed_time} seconds")


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = multiplication_pb2_grpc.MultiplicationStub(channel)
        print("-------------- ListMultipliers --------------")
        guide_list_multipliers(stub)
        print("-------------- RecordMultiplication --------------")
        guide_record_multiplication(stub)


if __name__ == "__main__":
    logging.basicConfig()
    run()
