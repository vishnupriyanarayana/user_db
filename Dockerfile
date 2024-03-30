# Use an official Python runtime as a base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the Flask application code into the container

COPY . .
# Install any needed dependencies specified in requirements.txt
RUN pip install -r requirements.txt

# Expose the port that the Flask application will run on
EXPOSE 5000

# Run the Flask application when the container launches
CMD ["python", "flask_db.py"]