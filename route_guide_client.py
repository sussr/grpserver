"""The Python implementation of the gRPC route guide client."""

from __future__ import print_function

import logging
import random

import grpc
import route_guide_pb2
import route_guide_pb2_grpc
import route_guide_resources


def make_number_note(message, number):
    return route_guide_pb2.RouteNote(
        message=message,
        number=route_guide_pb2.Point(number=number),
    )


def format_point(point):
    # not delegating in point.__str__ because it is an empty string when its
    # values are zero. In addition, it puts a newline between the fields.
    return "number: %d" % point.number


def guide_get_one_feature(stub, point):
    feature = stub.GetFeature(point)
    if not feature.number:
        print("Server returned incomplete feature")
        return

    if feature.name:
        print(
            "Feature called %r at %s"
            % (feature.name, format_point(feature.number))
        )
    else:
        print("Found no feature at %s" % format_point(feature.number))


def guide_get_feature(stub):
    guide_get_one_feature(
        stub, route_guide_pb2.Point(number=14)
    )
    guide_get_one_feature(stub, route_guide_pb2.Point(number=1))


def guide_list_features(stub):
    rectangle = route_guide_pb2.Rectangle(
        lo=route_guide_pb2.Point(number=1),
        hi=route_guide_pb2.Point(number=10),
    )
    print("Looking for features between 1 and 10")

    features = stub.ListFeatures(rectangle)


def generate_route(feature_list):
    for _ in range(0, 13):
        random_feature = random.choice(feature_list)
        print("Visiting point %s" % format_point(random_feature.number))
        yield random_feature.number


def guide_record_route(stub):
    feature_list = route_guide_resources.read_route_guide_database()

    route_iterator = generate_route(feature_list)
    route_summary = stub.RecordRoute(route_iterator)
    print("Finished trip with %s points " % route_summary.point_count)
    print("Passed %s features " % route_summary.feature_count)
    print("Multiplication of all numbers equals %s " % route_summary.multiplication_result)
    print("It took %s seconds " % route_summary.elapsed_time)


def generate_messages():
    messages = [
        make_number_note("First message", 1),
        make_number_note("Second message", 2),
        make_number_note("Third message", 3),
        make_number_note("Fourth message", 4),
        make_number_note("Fifth message", 5),
    ]
    for msg in messages:
        print("Sending %s at %s" % (msg.message, format_point(msg.number)))
        yield msg


def guide_route_chat(stub):
    responses = stub.RouteChat(generate_messages())
    for response in responses:
        print(
            "Received message %s at %s"
            % (response.message, format_point(response.number))
        )


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = route_guide_pb2_grpc.RouteGuideStub(channel)
        print("-------------- GetFeature --------------")
        guide_get_feature(stub)
        print("-------------- ListFeatures --------------")
        guide_list_features(stub)
        print("-------------- RecordRoute --------------")
        guide_record_route(stub)
        print("-------------- RouteChat --------------")
        guide_route_chat(stub)


if __name__ == "__main__":
    logging.basicConfig()
    run()
