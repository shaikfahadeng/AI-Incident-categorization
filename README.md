# 🚀 AI Incident Categorization & SRE Reliability Monitoring Platform

An end-to-end AI-powered incident classification and Site Reliability Engineering (SRE) monitoring system built using FastAPI, Machine Learning, and DevOps automation practices.

This project simulates a real production reliability platform that measures service health, tracks SLO compliance, detects incidents automatically, and sends alert notifications.

---

## 🎯 Project Objective

Modern cloud systems require continuous monitoring, incident detection, and automated reliability tracking.

This project demonstrates how to:

- Classify incidents using Machine Learning
- Track system reliability using SLI / SLO
- Monitor error budgets
- Detect service degradation
- Trigger automated alerting
- Implement DevOps CI/CD pipeline
- Containerize applications for deployment

---

## 🧠 Core Features

### 🤖 AI Incident Classification
- Machine learning model categorizes incidents
- TF-IDF vectorization + Logistic Regression
- REST API prediction endpoint

### 📊 SRE Reliability Monitoring
- Tracks total and failed requests
- Calculates service success rate (SLI)
- Evaluates reliability target (SLO)
- Computes remaining error budget

### 🚨 Automated Incident Detection
- Background monitoring thread
- Detects SLO breaches
- Triggers alerts automatically

### 📧 Email Alerting System
- Gmail SMTP integration
- Real-time SRE incident notifications
- Alert sent when reliability drops below target

### ⚙ DevOps CI/CD Pipeline
- Automated dependency installation
- Container build using Docker
- Azure DevOps pipeline integration

### 🐳 Containerized Deployment
- Dockerized FastAPI service
- Ready for cloud deployment

---

## 🏗 System Architecture

Client Request  
   ↓  
FastAPI Application  
   ↓  
Machine Learning Prediction  
   ↓  
Metrics Tracking (Requests / Failures)  
   ↓  
SLO Evaluation Engine  
   ↓  
Background Monitoring Thread  
   ↓  
Alert Trigger System  
   ↓  
Email Notification  

---

## 🧩 Technology Stack

| Category | Tools |
|---|---|
| Backend | FastAPI, Python |
| Machine Learning | Scikit-learn, TF-IDF |
| Monitoring | Custom SLI/SLO tracking |
| Alerting | SMTP Email |
| DevOps | Azure DevOps Pipelines |
| Containerization | Docker |
| Configuration | python-dotenv |
| API Docs | Swagger UI |

---

## 📂 Project Structure
