# ✅ Use official Python image
FROM python:3.10

# 🏗 Set working directory
WORKDIR /app

# 📂 Copy everything
COPY . /app

# 🧪 Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 🚪 Expose Streamlit default port
EXPOSE 8501

# ▶️ Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
