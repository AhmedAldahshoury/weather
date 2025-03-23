# Weather Forecast Application

This project provides a RESTful API for retrieving weather forecasts and managing city data. Built with Flask and Microsoft SQL Server (MSSQL), the application is containerized using Docker and orchestrated with Docker Compose.

## Features

- **City Management**: Add or remove cities from the database.
- **Weather Forecast Retrieval**: Fetch weather forecasts for the cities.
- **Automated Forecast Updates**: Scheduled tasks to update forecasts periodically.
- **Interactive API Documentation**: Swagger UI integration for easy API exploration.
- **Basic UI**: User Interface for basic information visualization.

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: Microsoft SQL Server (MSSQL)
- **Containerization**: Docker & Docker Compose
- **Scheduling**: APScheduler
- **API Documentation**: Flasgger (Swagger UI)

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [OpenWeatherMap API Key](https://openweathermap.org/api)

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/AhmedAldahshoury/weather.git
   cd weather
   ```

2. **Environment Configuration**:

   Create a `.env` file in the project root with the following content:

   ```env
   SA_PASSWORD=[Password]
   OPENWEATHERMAP_API_KEY=[KEY]
   ```

   Replace `[Password]` with a secure password of your choice for mssql.
   Replace `[Key]` with your api key for OpenWeatherMap.


3. **Build and Start the Containers**:

   Use Docker Compose to build and run the application:

   ```bash
   docker-compose up --build -d
   ```


5. **Access the Application**:
   - **Basic UI**: `http://localhost:3000`
   - **API Endpoints**: `http://localhost:5000`
   - **Swagger UI**: `http://localhost:5000/apidocs`

## API Endpoints

For complete guide, visit http://localhost:5000/apidocs to access the documentations or see docs. 


## Scheduled Tasks

The application uses APScheduler to automatically update weather forecasts every 10 seconds. This interval can be adjusted in the scheduler configuration.


## Future Work and Improvements

- **User Interface (UI)**: Update the UI to include more features.
- **Enhanced CI/CD**: Implement automated deployment workflows, including deployment to cloud services like AWS or Azure.
- **Comprehensive Testing**: Generate tests to include integration and end-to-end testing to further ensure application reliability.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure that your code adheres to the project's coding standards and passes all tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

*This project is maintained by [Ahmed Aldahshoury](https://github.com/AhmedAldahshoury).*

