FROM python:3.9-slim

WORKDIR /app

# העתק את ה־requirements מתוך התיקייה api-service
COPY api-service/requirements.txt . 

RUN pip install --no-cache-dir -r requirements.txt

# צור תיקייה לסקריפט
RUN mkdir scripts

# העתק את הסקריפט מתוך scripts/
COPY scripts/fetch_characters.py scripts/fetch_characters.py

# העתק את הקוד של ה־API
COPY api-service/app.py .

# העתק את סקריפט הבריאות
COPY api-service/healthcheck.sh .
RUN chmod +x healthcheck.sh

EXPOSE 80

CMD ["python", "app.py"]
