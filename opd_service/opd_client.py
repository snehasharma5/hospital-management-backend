import grpc
import opd_pb2
import opd_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = opd_pb2_grpc.OpdServiceStub(channel)
        response = stub.BookAppointment(opd_pb2.AppointmentRequest(
            patient_id="P001", doctor_id="D001", time="2025-05-14 10:00"
        ))
        print("Appointment:", response)

if __name__ == '__main__':
    run()
