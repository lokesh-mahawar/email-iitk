# 📧 Smart Email Assistant for Academic Deadlines

This is my personal implementation of an **email classification and deadline extraction system** designed for IITK academic emails.  
It fetches emails, classifies them into categories, and extracts assignment/quiz deadlines for calendar integration.  

For detailed explanation check the code and project notes. For a short introduction, see below.  

---

## 📝 Notes
1. This project is a **prototype** built mainly for academic productivity — not a production-grade email client.  
2. The classification uses a **hybrid approach**:  
   - Rule-based filters (keywords like "quiz", "assignment").  
   - ML model (**Logistic Regression + TF-IDF**) trained on labeled data.  
3. Deadline extraction currently relies on **regex parsing**. For more robust performance, an **NLP-based date extractor** can be added.  
4. Email fetching works with IITK’s POP3 server. For real-world deployment, support for OAuth/IMAP should be implemented.  

---

## 🚀 Features
- Fetches academic emails automatically.  
- Classifies emails into **Course-related, General Info, Scrap**.  
- Extracts deadlines (dates/times) from email body.  
- Provides API endpoints using **Flask/FastAPI**.  
- Supports **incremental retraining** with new labeled data.  

---

## 🔧 To Do
- Add push notifications for new deadlines.  
- Improve date extraction using NLP/transformer models.  
- Extend to other mail providers (IMAP, Gmail API).  
- Add frontend (Flutter/React Native) for mobile use.  
- Multi-user support with database integration.  

---

## ⚡ Example
**Input Email:**  
`"Quiz 2 for ESC201 is scheduled on 14th March 2025, 8:00 PM in L7."`  

**Output:**  
```json
{
  "category": "Course-related",
  "deadline": "14-03-2025 20:00"
}
