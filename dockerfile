# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app's code into the container
COPY . .

# Expose the port your app runs on (e.g., 5000, 8000, 8080)
# Make sure your app.py runs on this port!
# E.g., app.run(host='0.0.0.0', port=8080)
EXPOSE 8080

# Command to run your application
# Assumes your file is named 'app.py' and your Flask object is named 'app'
# Change 'app:app' if your file/variable names are different
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
