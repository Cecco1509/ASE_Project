
# ASE Project: Gacha Collection Backend

## Table of Contents
- [General Description](#general-description)
  - [Key Features](#key-features)
  - [Microservices Overview](#microservices-overview)
- [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation and Execution](#installation-and-execution)
  - [Running Unit Tests](#running-unit-tests)
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

-   **AdminGacha**: Manages the gacha collection, allowing administrators to add, update, and delete gacha items.
-   **PlayerGacha**: Provides functionalities for players to view and roll gacha items, as well as participate in the auction market.
- **Admin Auth**: Admin registration, login, and logout.
- **Player Auth**: Player registration, login, and logout.
- **Admin Players**: Admin view and management of player profiles.
- **Player Profile**: Player view and update of their profile.
- **Admin Currency**: View player currency transaction history.
- **Player Currency**: In-game currency purchase and viewing player transaction history.
- **Admin Market**: Admin view and modification of auction details and market history.
- **Player Market**: Player auction market for creating and bidding on auctions.
- **Admin Gacha**: Admin view and management of the gacha collection.
- **Player Gacha**: Player gacha collection management and item rolls.
- **API Gateway**: Centralized entry point for all requests, routes requests to respective microservices.
- **DB Managers**: Database management services for each microservice.

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
    
The main API gateway should be accessible at `http://localhost:5000`.
For example, to access the AdminGacha service:
```        
GET http://localhost:5000/api/admin/gacha
```
        
 -  **Stopping the Application**:
    
To stop the application and remove containers, run:

    docker-compose down
    
### Running Unit Tests

 - Run the mock microservices: Each microservice has a test code and a test docker file that allows it to run the requests on mock data instead of real data from the database. For example, to run the admin gacha microservice in test mode, you have to run the following commands:

```
docker build -t gachadmin_test -f ./GatchasAdmin/dockerfile_test .
docker run -p 5000:5000 gachadmin_test
```

 -   **Postman Collection**: Use the included Postman collections in the "doc" folder to run unit tests for each microservice and each endpoint.

### API Documentation

The API is documented using OpenAPI, with an `openapi.yaml` file located in the "doc" folder. You can view the documentation with tools like **Swagger UI**.

