import grpc
import auth_pb2 as auth_pb2
import auth_pb2_grpc as auth_pb2_grpc

def test():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = auth_pb2_grpc.AuthServiceStub(channel)

        # Register
        try:
            register_response = stub.Register(auth_pb2.RegisterRequest(
                username="testuser1234",
                password="testpass1",
                role="admin"
            ))
            print("Register response:", register_response)
        except grpc.RpcError as e:
            print("Register failed:", e.details())

        # Login
        try:
            login_response = stub.Login(auth_pb2.LoginRequest(
                username="testuser1234",
                password="testpass1"
            ))
            print("Login response:", login_response)
        except grpc.RpcError as e:
            print("Login failed:", e.details())

if __name__ == "__main__":
    test()
