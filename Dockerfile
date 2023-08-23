
# Use the official Ubuntu as a parent image
FROM --platform=linux/amd64 ubuntu:20.04


# Set maintainer label
LABEL maintainer="your-email@example.com"



# # Update and install required software

RUN apt-get update
RUN apt-get install -y wget


# # Download and install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p miniconda3 && \
    rm miniconda.sh

# # Set path to conda
ENV PATH /miniconda3/bin:$PATH

COPY . bank_chatbot/

# # Create conda environment using environment.yml
RUN conda env create -f bank_chatbot/environment.yml

# # Expose the desired port for the app
EXPOSE 5000

CMD ["miniconda3/envs/bank_chatbot/bin/python", "bank_chatbot/app.py"]