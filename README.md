# **Reddit Real-Time Sentiment Analysis**

## **Project Overview**  
This project enables real-time sentiment and topic classification on Reddit comments using Apache Kafka, Streamlit, and various NLP models.  

---

## **Key Features**  
- 🚀 **Real-Time Data Streaming**: Streams Reddit comments in real-time using Apache Kafka.  
- 🤖 **Sentiment Analysis**: Analyzes the sentiment of comments using:  
  - A pretrained model: [Twitter Roberta Sentiment Model](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment).  
  - A custom model built from scratch using SVD.  
- 📚 **Topic Classification**: Identifies the main topics in comments with [BART Large MNLI](https://huggingface.co/facebook/bart-large-mnli).  
- 📊 **Interactive Dashboard**: Visualizes results on an interactive Streamlit dashboard.  

---

## **Technologies Used**  
- **Apache Kafka**: Real-time data streaming platform.  
- **Streamlit**: For building interactive data visualization dashboards.  
- **NLP Models**: Pretrained models from Hugging Face, as well as custom models using libraries like Scikit-learn, Transformers, and NLTK.  

---

## **Setup Instructions**

### 1️⃣ **Set Up a Virtual Environment**  
Follow these steps to set up and manage a virtual environment:  

- **Create the virtual environment:**  
  ```bash
  python -m venv venv
  ```  
- **Activate the virtual environment:**  
  ```bash
  source venv/bin/activate
  ```  
- **Install dependencies:**  
  ```bash
  pip install -r requirements.txt
  ```  
- **Deactivate the virtual environment:**  
  ```bash
  deactivate
  ```  

**Useful Commands for Package Management:**  
- Install a package:  
  ```bash
  pip install <package>
  ```  
- Uninstall a package:  
  ```bash
  pip uninstall <package>
  ```  
- List installed packages:  
  ```bash
  pip list
  ```  

---

### 2️⃣ **Set Up API Keys**

Store your Reddit API credentials securely in a `.env` file. Create a file named `.env` in the root directory of your project and add your credentials, in the format of the .env-example file at the root of the project.

---

### 3️⃣ **Set Up Apache Kafka**  

To run Kafka for this project:  

- **Start Zookeeper:**  
  ```bash
  bin/zookeeper-server-start.sh config/zookeeper.properties
  ```  
- **Start Kafka Server:**  
  ```bash
  bin/kafka-server-start.sh config/server.properties
  ```  
- **Create Kafka Topics:**  
  ```bash
  bin/kafka-topics.sh --create --topic reddit_topic --bootstrap-server localhost:9092
  bin/kafka-topics.sh --create --topic reddit_transform --bootstrap-server localhost:9092
  ```  

---

### 4️⃣ **Run the Project**

To run the main script, follow these steps:  

1. Run the main script with the desired argument (`scratch` or `pretrained`):  
   ```bash
   python3 source/main.py <argument>
   ```  
   Replace `<argument>` with either `scratch` or `pretrained`.  

2. Wait for a few moments to allow data to populate Kafka topics.  

3. Launch the Streamlit dashboard to visualize the results:  
   ```bash
   streamlit run source/dashboard/streamlit_dashboard.py
   ```  

4. In case of an error caused by a package not found:
   ```bash
   export PYTHONPATH=$(pwd)
   ```  

💡 **Tip**: Wait a few seconds before starting the Streamlit dashboard to allow for better visualizations with more data.  

---

### 5️⃣ **Potential Improvements**

Here are some possible enhancements for the project:  
- 🔍 Add advanced search functionality to filter comments by subreddit.  
- 📈 Implement trend analysis for better insights into sentiment over time.  
- ✅ Include a testing phase to validate the models' performance.  

---

## **References**  

- **Sentiment Analysis Model**: [Twitter Roberta Sentiment Model](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment)  
- **Topic Classification Model**: [BART Large MNLI](https://huggingface.co/facebook/bart-large-mnli)  
- **NLP Courses by Mathieu Labeau**  

---
