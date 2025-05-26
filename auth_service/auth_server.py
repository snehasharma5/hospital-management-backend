from concurrent import futures
import grpc
import auth_pb2 as auth_pb2
import auth_pb2_grpc as auth_pb2_grpc
from database import SessionLocal
from models.user import User, UserRole
from utils.security import hash_password, verify_password
from utils.token import create_jwt_token

class AuthService(auth_pb2_grpc.AuthServiceServicer):
    def Register(self, request, context):
        db = SessionLocal()
        if db.query(User).filter_by(username=request.username).first():
            context.set_details("Username already exists")
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            return auth_pb2.UserResponse()

        user = User(
            username=request.username,
            password_hash=hash_password(request.password),
            role=UserRole[request.role.upper()]
        )
        db.add(user)
        db.commit()
        return auth_pb2.UserResponse(username=user.username, role=user.role.value)

    def Login(self, request, context):
        db = SessionLocal()
        user = db.query(User).filter_by(username=request.username).first()
        if not user or not verify_password(request.password, user.password_hash):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details("Invalid username or password")
            return auth_pb2.LoginResponse()

        token = create_jwt_token(user.username, user.role.value)
        return auth_pb2.LoginResponse(token=token, role=user.role.value)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("AuthService running on port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
