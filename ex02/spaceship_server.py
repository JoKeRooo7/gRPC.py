from concurrent import futures

import spaceship_pb2 as spaceship_messages
import spaceship_pb2_grpc as spaceship_service
import spaceships_config
import random
import grpc


class SpaceshipServicer(spaceship_service.SpaceshipServiceServicer):
    def get_spaceships(self, request, context):
        return self.generate_spaceships()

    def generate_spaceships(self):
        for _ in range(random.randint(1, 10)):
            ship = spaceship_messages.Spaceship()

            ship.alignment = random.choice([spaceship_messages.ALLY,
                                            spaceship_messages.ENEMY])
            ship.name = random.choice(spaceships_config.SHIPS_NAME)

            ship.class_ = random.choice([
                spaceship_messages.CORVETTE,
                spaceship_messages.FRIGATE,
                spaceship_messages.CRUISER,
                spaceship_messages.DESTROYER,
                spaceship_messages.CARRIER,
                spaceship_messages.DREADNOUGHT,
                ])

            ship.length = round(random.uniform(70, 21000), 1)
            ship.crew_size = random.randint(2, 510)
            ship.armed = random.choice([True, False])

            for _ in range(random.randint(0, 10)):
                officer = ship.officers.add()
                officer.first_name = random.choice(
                    spaceships_config.FIRST_NAME)
                officer.last_name = random.choice(
                    spaceships_config.SECOND_NAME)
                officer.rank = random.choice(
                    spaceships_config.RANK)

            yield ship


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    spaceship_service.add_SpaceshipServiceServicer_to_server(
        SpaceshipServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


def main():
    serve()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
