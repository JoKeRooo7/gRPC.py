import argparse
import grpc
import spaceship_pb2 as spaceship_messages
import spaceship_pb2_grpc as spaceship_service
import json
import argparse
import spaceships_validation as sv

from psql.set_ships_in_db import (
    add_spaceship_in_db,
    find_traitors,
)


ALIGNMENT = {
    0: "Ally",
    1: "Enemy",
}


SHIP_CLASSES = {
    0: "Corvette",
    1: "Frigate",
    2: "Cruiser",
    3: "Destroyer",
    4: "Carrier",
    5: "Dreadnought",
}


def run_client(coordinates):
    output: bool = False
    channel = grpc.insecure_channel("localhost:50051")
    stub = spaceship_service.SpaceshipServiceStub(channel)

    request = spaceship_messages.Coordinates(coordinates=coordinates)
    response_iterator = stub.get_spaceships(request)

    for response in response_iterator:
        spaceship_dict = {
            "alignment": bool(response.alignment),
            "name": response.name,
            "class_": SHIP_CLASSES.get(response.class_, "Unknown"),
            "length": round(response.length, 1),
            "crew_size": response.crew_size,
            "armed": response.armed,
            "officers": [
                {
                    "first_name": officer.first_name,
                    "last_name": officer.last_name,
                    "rank": officer.rank,
                }
                for officer in response.officers
            ],
        }
        try:
            sv.Spaceship(**spaceship_dict)

            spaceship_dict["alignment"] = ALIGNMENT.get(
                spaceship_dict["alignment"])

            add_spaceship_in_db(spaceship_dict)

            print(json.dumps(spaceship_dict, indent=2, separators=(',', ': ')))
            output = True

        except sv.ValidationError as e:
            # print(f"Error: {e}")
            continue

    return output


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    scan_parser = subparsers.add_parser("scan")
    scan_parser.add_argument("coordinates", nargs='+', type=float)

    subparsers.add_parser("list_traitors")

    args = parser.parse_args()

    if args.command == "scan":
        coordinates = args.coordinates
        # print(" ...поиск...")
        while True:
            if run_client(coordinates):
                break

    elif args.command == "list_traitors":
        find_traitors()


if __name__ == "__main__":
    main()
