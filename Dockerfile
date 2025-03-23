# Use Python base image
FROM python:3.9

# Set work directory
WORKDIR /app

# Install dependencies required for pyodbc and curl
RUN apt-get update && apt-get install -y unixodbc-dev curl gnupg apt-transport-https

# Download the package to configure the Microsoft repo
RUN curl -sSL -O https://packages.microsoft.com/config/debian/$(grep VERSION_ID /etc/os-release | cut -d '"' -f 2 | cut -d '.' -f 1)/packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    rm packages-microsoft-prod.deb

# Update apt repository and install the Microsoft ODBC driver and tools
RUN apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 mssql-tools18 unixodbc-dev libgssapi-krb5-2

# Add mssql-tools18 to the PATH environment variable
ENV PATH="$PATH:/opt/mssql-tools18/bin"

# Copy application code
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the wait script into the container
COPY wait-for-sql.sh /wait-for-sql.sh
RUN chmod +x /wait-for-sql.sh

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV PYTHONPATH=/app

# Expose the Flask application port
EXPOSE 5000

# Command to run migrations and the app
CMD /wait-for-sql.sh mssql_container 1433 sh -c "\
  flask db init || true && \
  flask db migrate -m 'Initial migration' && \
  flask db upgrade && \
  flask populate-db && \
  flask run --host=0.0.0.0"
