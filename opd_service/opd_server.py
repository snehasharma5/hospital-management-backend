import grpc
from concurrent import futures
import time

from opd_pb2 import AppointmentResponse, CancelResponse
import opd_pb2_grpc

class OpdService(opd_pb2_grpc.OpdServiceServicer):
    def BookAppointment(self, request, context):
        print(f"Booking appointment for {request.patient_id}")
        return AppointmentResponse(appointment_id="opd123", status="Booked")

    def CancelAppointment(self, request, context):
        print(f"Cancelling appointment {request.appointment_id}")
        return CancelResponse(status="Cancelled")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    opd_pb2_grpc.add_OpdServiceServicer_to_server(OpdService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("OpdService running on port 50052")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
