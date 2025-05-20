import grpc
from concurrent import futures
import time

import auth_pb2
import auth_pb2_grpc
from db import SessionLocal
from models.user import User
from utils.hash import hash_password, verify_password
from utils.jwt import create_token

class AuthService(auth_pb2_grpc.AuthServiceServicer):
    def Register(self, request, context):
        session = SessionLocal()
        existing = session.query(User).filter(User.username == request.username).first()
        if existing:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("Username already taken.")
            return auth_pb2.AuthResponse()

        user = User(
            username=request.username,
            password_hash=hash_password(request.password),
            role=request.role.upper()
        )
        session.add(user)
        session.commit()
        return auth_pb2.AuthResponse(message="User registered successfully.")

    def Login(self, request, context):
        session = SessionLocal()
        user = session.query(User).filter(User.username == request.username).first()
        if not user or not verify_password(request.password, user.password_hash):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details("Invalid credentials")
            return auth_pb2.LoginResponse()

        token = create_token(user.username, user.role)
        return auth_pb2.LoginResponse(token=token)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    print("AuthService running on port 50053")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
