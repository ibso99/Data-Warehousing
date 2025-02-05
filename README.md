# 10 Academy: Artificial Intelligence Mastery - Week 7 Challenge

## Project: Building a Data Warehouse for Ethiopian Medical Business Data

**Date:** February 29 - March 4, 2024

---

## Overview

This project focuses on building a data warehouse to store and analyze data related to Ethiopian medical businesses scraped from Telegram channels. The goal is to develop a robust and scalable solution that integrates data scraping, cleaning, transformation, object detection using YOLO, and data warehousing best practices. Additionally, the collected data will be exposed through a FastAPI service.

## Business Need

Kara Solutions, a leading data science company, requires a centralized data warehouse to analyze Ethiopian medical business data. This will enable comprehensive insights, trend identification, and improved decision-making for their clients.

## Core Tasks

1. **Data Scraping and Collection:** Extract relevant data from Telegram channels.
2. **Data Cleaning and Transformation:** Process and structure scraped data for analysis.
3. **Object Detection Using YOLO:** Implement YOLO for object detection in images from Telegram.
4. **Data Warehouse Design and Implementation:** Create a scalable data storage solution.
5. **Data Integration and Enrichment:** Enhance the collected data for deeper insights.
6. **API Development with FastAPI:** Provide easy access to processed data.

---

## Deliverables

### Task 1: Data Scraping and Collection Pipeline

**Objective:** Extract data from Telegram channels and store it for further processing.

#### Steps:
1. **Telegram Scraping:**
   - Use the Telegram API (`telethon`) or custom scripts to extract data.
   - Targeted channels:
     - [DoctorsET](https://t.me/DoctorsET)
     - Chemed (Link needed)
     - [Lobelia4Cosmetics](https://t.me/lobelia4cosmetics)
     - [Yetenaweg](https://t.me/yetenaweg)
     - [EAHCI](https://t.me/EAHCI)
     - More channels from [TGStat](https://et.tgstat.com/medicine)
   - **Tools:** `telethon` (Python library for Telegram API)

2. **Image Scraping:**
   - Extract images from Chemed, Lobelia4Cosmetics, and other relevant channels.

3. **Raw Data Storage:**
   - Store text and images in a temporary storage location (e.g., local database, files).

4. **Monitoring and Logging:**
   - Implement logging to track scraping progress and capture errors.

---

### Task 2: Data Cleaning and Transformation

**Objective:** Clean and structure the scraped data for integration into the data warehouse.

#### Steps:
1. **Data Cleaning:**
   - Remove duplicates and handle missing values.
   - Standardize formats (e.g., dates, units of measure).
   - Validate data integrity.

2. **Storing Cleaned Data:**
   - Save processed data in a database (e.g., PostgreSQL, MySQL).

3. **Data Transformation Using DBT:**
   - Install DBT:
     ```bash
     pip install dbt-core dbt-postgres
     dbt init my_project
     ```
   - Define models:
     ```sql
     {{ config(materialized='table') }}
     SELECT business_id, business_name FROM {{ source('raw_data', 'businesses') }}
     ```
   - Run transformations:
     ```bash
     dbt run
     ```
   - Perform testing and documentation:
     ```bash
     dbt test
     dbt docs generate
     dbt docs serve
     ```

4. **Monitoring and Logging:**
   - Implement logging to track transformations and capture errors.

---

### Task 3: Object Detection Using YOLO

**Objective:** Detect objects in scraped images using YOLO.

#### Steps:
1. **Setup Environment:**
   ```bash
   pip install opencv-python torch torchvision torchaudio
   git clone https://github.com/ultralytics/yolov5.git
   cd yolov5
   pip install -r requirements.txt
   ```

2. **Run Object Detection:**
   ```python
   import torch
   model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
   img = 'path/to/your/image.jpg'
   results = model(img)
   results.print()
   results.save()
   ```

3. **Process Detection Results:**
   - Extract bounding box coordinates, confidence scores, and class labels.

4. **Store Detection Data:**
   - Save detected objects' metadata in a database.

5. **Monitoring and Logging:**
   - Track the object detection process and log errors.

---

### Task 4: Expose Data via FastAPI

**Objective:** Develop a REST API to provide easy access to the processed data.

#### Steps:
1. **Setup Environment:**
   ```bash
   pip install fastapi uvicorn sqlalchemy psycopg2-binary
   ```

2. **Project Structure:**
   ```
   my_project/
   ├── main.py
   ├── database.py
   ├── models.py
   ├── schemas.py
   ├── crud.py
   ```

3. **Run FastAPI Application:**
   ```bash
   uvicorn main:app --reload
   ```

---

## Conclusion

This project demonstrates a complete pipeline for building a data warehouse solution to support Ethiopian medical business analysis. By integrating data scraping, transformation using DBT, object detection with YOLO, and API development with FastAPI, this solution provides a powerful framework for data-driven decision-making.

### Key Takeaways:
- **Data Pipeline Automation:** Streamlined extraction, cleaning, and transformation.
- **AI-powered Insights:** YOLO for object detection in medical business images.
- **Scalable Data Storage:** A structured data warehouse for long-term analysis.
- **API Accessibility:** FastAPI for easy data access and integration.

### Future Work:
- Improve object detection accuracy.
- Expand data sources for broader analysis.
- Enhance API functionality with advanced analytics.

By leveraging modern data engineering and AI techniques, this project converts raw data into actionable intelligence, driving better decision-making in the Ethiopian medical business sector.

