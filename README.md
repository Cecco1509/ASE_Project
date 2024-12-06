
# ASE Project: Gacha Collection Backend

## Table of Contents
- [General Description](#general-description)
  - [Key Features](#key-features)
  - [Microservices Overview](#microservices-overview)
- [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation and Execution](#installation-and-execution)
  - [Running Unit Tests](#running-unit-tests)
  - [Running Integration Tests](#running-integration-tests)
  - [Running Locust Tests](#running-locust-tests)
- [API Documentation](#api-documentation)

---

## General Description

The ASE Project is a backend application designed to manage a digital "Gacha" collection system, where players can collect, view, and trade unique items. The backend is developed using a microservices architecture, with each service responsible for specific parts of the application's functionality.
The primary users of this backend are:

-   **Players**: Users who collect and trade gacha items using in-game currency.
-   **Administrators**: Users with full control over the system, including player management, gacha collection updates, and auction monitoring.

### Key Features

-   **Distributed Microservices Architecture**: Each microservice operates independently and communicates via HTTP requests.
-   **REST API Interface**: A well-defined RESTful API for each microservice.
-   **Data Persistence**: Integration with a MySQL database for storing the data.
-   **Security Mechanisms**: Basic input sanitization and separate access for players and administrators.
-   **Unit and Performance Testing**: Endpoints are unit tested, with performance testing configured.
-   **Docker-Based Deployment**: Each microservice is containerized for easy deployment and scalability.

### Microservices Overview

- **ApiGatewayAdmin**: Handles all admin-related requests and routes them to the appropriate microservices.
- **ApiGatewayPlayer**: Handles all player-related requests and routes them to the appropriate microservices.
- **AuthMicroservice**: Handles authentication operations like registration, login, and logout, generating and validating access tokens for both admins and players.
- **AuctionDBManager**: Manages the database for auctions, including creating, updating, and retrieving auction data.
- **AuctionsMicroservice**: Handles auction operations for both admins and players, such as bidding and auction creation.
- **Auctioneer**: Checks if there are any open auctions that need to be closed and sends a request to the AuctionsMicroservice to handle them.
- **GachaDBManager**: Manages the database for gacha items, including item creation, updates, and retrieval.
- **GachaMicroservice**: Provides player and admin functionalities for gacha operations, such as rolling and managing items.
- **PaymentsDBManager**: Manages the database for in-game currency transactions, including purchases and refunds.
- **PaymentsMicroservice**: Handles in-game currency transactions, including player purchases and refunds.
- **TransactionsDBManager**: Manages the database for player transaction history and records of in-game activities.
- **TransactionsMicroservice**: Handles player transaction records and ensures data consistency for all in-game activities.
- **UsersDBManager**: Manages the database for player and admin profiles, including authentication and profile updates.
- **UsersMicroservice**: Provides functionalities for player and admin account management, including registration and login.

## Quick Start

### Prerequisites

-   **Docker** and **Docker Compose**: Ensure Docker and Docker Compose are installed on your system.
-   **Python 3.12** (if running locally for development): Install required packages from `requirements.txt`.

### Installation and Execution

 -  **Clone the Repository**:

```
git clone https://github.com/your-repo/ASE-Project.git
cd ASE-Project
```
        
 -  **Build and Run the Docker Containers**:
    
   Use Docker Compose to build and run the microservices in containers.
    
    docker-compose up --build
    
 -  **Accessing the API**:
    
The API gateways are accessible at the following ports:

- **Player Gateway**: `https://localhost:5000`
- **Admin Gateway**: `https://localhost:5001`

For example:
```
# Player Gateway Example
GET https://localhost:5000/api/player/gacha/system-collection

# Admin Gateway Example
GET https://localhost:5001/api/admin/gacha
```
        
 -  **Stopping the Application**:
    
To stop the application and remove containers, run:

    docker-compose down
    
### Running Unit Tests

 - Unit tests are automatically executed using a GitHub Actions workflow. This workflow is triggered each time changes are pushed to the `main` branch. The workflow runs tests for all microservices using Postman collections and mock data to ensure endpoint functionality.
 - If you want to manually execute the unit tests in isolation, follow these steps:
  1. **Run the mock microservices:** Each microservice includes a test Docker file and mock data. For example, to run the Gacha Microservice in test mode, just execute the following commands in the root folder "ASE_Project":

```
docker build -t gachams_test -f ./GachaMicroservice/dockerfile_test .
docker run --rm --name gachams_test_ -p 5000:5000 gachams_test
```

  2. **Run Postman Tests:** Use the Postman collections in the "doc/postman" folder to run unit tests for each microservice and its endpoints.

Example: Open Postman and import the appropriate collection (e.g., GachaMicroservice.postman_collection.json) and run the collection in the Postman runner.

### Running Integration Tests

- Run the real microservices: All the microservices can be called using the docker compose command from the root folder "ASE_Project":
  
  ```
  docker compose up --build
  ```

-   **Postman Collection**: Use the included Postman collection `Integration_tests.postman_collection.json`, which is included in the "docs/postman" folder, to run all the integration tests.
  ### Running Performance Tests

- Run the real microservices with bottle necks scaled up using this command:
  ```
  docker-compose up --scale authmicroservice=6 --scale paymentsmicroservice=3 --scale gachamicroservice=3 -d
  ```
 **Locust test**: Run the locust command in the docs folder where the locustfile.py tests are located.
 
### API Documentation

- **Microservices OpenAPI Specifications**:
  - `dbmanagers.openapi.yaml`
  - `gateways.openapi.yaml`
  - `services.openapi.yaml`
- The documentation is available in the "doc" folder and can be visualized using tools like Swagger UI.  

