FROM gcr.io/dataflow-templates-base/python3-template-launcher-base 

#Setting Working Directory for Docker Container
ARG WORKDIR=/template
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}

# Due to a change in the Apache Beam base image in version 2.24, you must to install
# libffi-dev manually as a dependency. For more information:
# https://github.com/GoogleCloudPlatform/python-docs-samples/issues/4891
RUN apt-get update && apt-get install -y libffi-dev && rm -rf /var/lib/apt/lists/*

#Copying pipeline python requirements file and pipeline code into the container
COPY requirements.txt .
COPY beam_flex_template_pipeline.py .

#Setting environment variables
ENV FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE="${WORKDIR}/requirements.txt"
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="${WORKDIR}/beam_flex_template_pipeline.py"

#Installing python packages required for pipeline code
RUN pip install -U -r ./requirements.txt