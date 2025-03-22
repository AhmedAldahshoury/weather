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

# Expose the Flask application port
EXPOSE 5000

# Command to run the app
CMD ["python", "app/main.py"]
