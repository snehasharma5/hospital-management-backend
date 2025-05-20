# Hospital Management System Backend

A microservices-based backend for a hospital management application, using **gRPC** and **Python**.

---

## Services

| Service       | Description                            | Port   |
|---------------|----------------------------------------|--------|
| `auth_service`| Handles user login, registration, JWTs | `50051`|
| `user_service`| Manages user details and roles         | `50052`|
| `ipd_service` | Handles inpatient operations           | `50053`|
| `opd_service` | Handles outpatient operations          | `50054`|

---

## Project Structure

hospital-management/
│
├── auth_service/
│ ├── auth_server.py
│ ├── protos/auth.proto
│ └── ...
│
├── user_service/
│ ├── user_server.py
│ ├── protos/user.proto
│ └── ...
│
├── ipd_service/
│ ├── ipd_server.py
│ ├── protos/ipd.proto
│ └── ...
│
├── opd_service/
│ ├── opd_server.py
│ ├── protos/opd.proto
│ └── ...
│
├── shared/
│ ├── db.py # Shared DB connection utils
│ └── utils.py
│
└── README.md



---

#Requirements

- Python 3.10+
- `grpcio` and `grpcio-tools`
- SQLite or PostgreSQL for DB (as needed)

#Install dependencies:

```bash
pip install grpcio grpcio-tools protobuf

#Before running any service, compile the .proto files:
# Example for auth_service
cd auth_service
python -m grpc_tools.protoc -I=./protos --python_out=. --grpc_python_out=. protos/auth.proto

# Repeat similarly for user_service, ipd_service, opd_service

#Running the Services (Locally)
#In separate terminals, run each service:

# Terminal 1
cd auth_service
python auth_server.py

# Terminal 2
cd user_service
python user_server.py

# Terminal 3
cd ipd_service
python ipd_server.py

# Terminal 4
cd opd_service
python opd_server.py

#Each service listens on its own port (localhost:50051, 50052, etc.)
#You can test the services using:

    Sample client.py scripts in each service (optional)
    gRPC GUI tools like BloomRPC

#Authentication & Roles

    Users are registered via auth_service
    Roles (doctor, patient, admin, etc.) are managed via user_service
    JWT token validation can be enforced in ipd_service and opd_service
