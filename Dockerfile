# Select starting image
FROM python:3.10.0-slim

# Create user name and home directory variables. 
# The variables are later used as $USER and $HOME. 
ENV USER=username
ENV HOME=/home/$USER

# Add user to system
RUN useradd -m -u 1000 $USER

# Set working directory (this is where the code should go)
WORKDIR $HOME/app

# Update system and install dependencies.
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    software-properties-common \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy config file
#COPY .streamlit $HOME/.streamlit

# Copy all files that the app needs
COPY app/app.py $HOME/app/app.py
COPY app/requirements.txt $HOME/app/requirements.txt
COPY assets/Scilife_NBIS.jpg $HOME/app/assets/Scilife_NBIS.jpg
#COPY app/pages $HOME/app/pages/
COPY app/compute_snr.py $HOME/app/compute_snr.py
# Add more COPY commands here if you have other files to copy

# Install packages listed in requirements.txt with pip
RUN pip install --no-cache-dir -r requirements.txt

# Switch to the non-root user
USER $USER

# Expose the default Streamlit port
EXPOSE 8501

# Healthcheck for the running Streamlit service
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Entry point for running the Streamlit app
#ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--browser.gatherUsageStats=false"]
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

