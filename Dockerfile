FROM python:3.13.9-alpine

WORKDIR /app
# COPY . /app # we move this down for optimization (when we change the CMD or anything inside the file to not build the requirements.txt again and agian)

COPY requirements.txt .
RUN pip install -r requirements.txt

# Manual installation of prerelease of langchain (until it stabilizes v1)
RUN pip install --pre -U langchain
RUN pip install --pre -U langchain-openai

COPY . .

EXPOSE 8000

CMD ["streamlit", "run", "app.py"]