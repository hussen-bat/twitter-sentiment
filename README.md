# 🐦 Twitter Sentiment Analysis

A machine learning web application that classifies tweet sentiment as **Positive** or **Negative** in real-time, built with Flask and deployed on **AWS EC2**.

> **Author:** Hussen Shaikh

---

## ✨ Features

- **Real-time Sentiment Analysis** — Paste any tweet and get instant results
- **Confidence Score** — See how confident the model is with a visual progress bar
- **Character Counter** — Live 280-character limit tracker (just like Twitter)
- **Clean Dark UI** — Minimal, Twitter-inspired dark theme interface
- **Responsive Design** — Works seamlessly on desktop and mobile

---

## 🛠️ Tech Stack

| Layer       | Technology                         |
|-------------|------------------------------------|
| Frontend    | HTML, CSS, Jinja2                  |
| Backend     | Python, Flask                      |
| ML Model    | Logistic Regression (scikit-learn) |
| NLP         | NLTK (PorterStemmer, Stopwords)    |
| Vectorizer  | TF-IDF (scikit-learn)              |
| Deployment  | AWS EC2 (Gunicorn)                 |

---

## 📊 Dataset

- **Source:** [Sentiment140 (Stanford)](https://www.kaggle.com/datasets/kazanova/sentiment140)
- **Size:** 1.6 million tweets
- **Classes:** Balanced — 800K Negative, 800K Positive
- **Columns:** `target`, `id`, `date`, `flag`, `user`, `text`

---

## 🧠 How It Works

```
User Input (Tweet)
       │
       ▼
┌─────────────────────┐
│    Preprocessing    │  → Regex cleaning, lowercase, stopword removal, stemming
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│   TF-IDF Vectorizer │  → Convert text to numerical feature vector
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Logistic Regression │  → Predict sentiment + confidence probability
└──────────┬──────────┘
           ▼
    Positive / Negative (with confidence %)
```

### Preprocessing Pipeline
1. **Regex Cleaning** — Remove non-alphabetic characters
2. **Lowercasing** — Normalize text to lowercase
3. **Stopword Removal** — Filter out common English words (`the`, `is`, `and`, etc.)
4. **Stemming** — Reduce words to root form using Porter Stemmer

---

## 📁 Project Structure

```
Twitter-Sentiment-Analysis/
├── run.py                    # Flask web server & prediction logic
├── trained_model.sav         # Serialized Logistic Regression model
├── vectorizer.sav            # Serialized TF-IDF vectorizer
├── Twitter.ipynb             # Jupyter notebook (EDA + model training)
├── templates/
│   └── index.html            # Frontend UI template
├── appspec.yml               # AWS CodeDeploy config
├── requirements.txt          # Python dependencies
├── .gitignore                # Files excluded from Git tracking
└── README.md                 # You are here!
```

---

## 🚀 Local Setup

### Prerequisites
- Python 3.9+
- pip

```bash
# 1. Clone the repository
git clone https://github.com/hussen-bat/twitter-sentiment.git
cd twitter-sentiment

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python run.py
```

Open **http://localhost:5000** in your browser.

---

## ☁️ Deployment on AWS EC2


### Step 1 — Launch an EC2 Instance

1. Log in to [AWS Console](https://console.aws.amazon.com)
2. Go to **EC2** → **Launch Instance**
3. Configure:

| Setting          | Value                          |
|------------------|-------------------------------|
| **Name**         | `twitter-sentiment`           |
| **AMI**          | Ubuntu Server 22.04 LTS (Free tier eligible) |
| **Instance Type**| `t3.micro` (or `t2.micro`)    |
| **Key Pair**     | Create new → download `.pem` file (keep it safe!) |
| **Security Group** | Allow **SSH (port 22)** and **Custom TCP (port 5000)** from Anywhere (0.0.0.0/0) |
| **Storage**      | 8 GB (default is fine)        |

4. Click **"Launch Instance"**

---

### Step 2 — Connect to Your EC2 Instance

Open your terminal and connect via SSH:

```bash
# Give permission to your key file (Mac/Linux only)
chmod 400 your-key.pem

# Connect (replace with your EC2 Public IP)
ssh -i "your-key.pem" ubuntu@<YOUR_EC2_PUBLIC_IP>
```

> Find your Public IP in EC2 → Instances → click your instance → **Public IPv4 address**

---

### Step 3 — Set Up the Server

Run these commands inside your EC2 instance:

```bash
# Update packages
sudo apt update && sudo apt upgrade -y

# Install Python, pip, and git
sudo apt install python3-pip git -y

# Clone your GitHub repository
git clone https://github.com/hussen-bat/twitter-sentiment.git
cd twitter-sentiment

# Install Python dependencies
pip3 install -r requirements.txt
```

---

### Step 4 — Upload Model Files

Your `.sav` files are too large for GitHub. Upload them directly from your local machine using SCP:

```bash
# Run this from your LOCAL machine terminal (not EC2)
scp -i "your-key.pem" trained_model.sav ubuntu@<YOUR_EC2_PUBLIC_IP>:/home/ubuntu/Twitter-Sentiment-Analysis/
scp -i "your-key.pem" vectorizer.sav ubuntu@<YOUR_EC2_PUBLIC_IP>:/home/ubuntu/Twitter-Sentiment-Analysis/
```

---

### Step 5 — Run the App

```bash
# Inside EC2 — start the app in background
cd /home/ubuntu/Twitter-Sentiment-Analysis
nohup gunicorn run:app --bind 0.0.0.0:5000 > app.log 2>&1 &
```

Your app is now live at:
```
http://<YOUR_EC2_PUBLIC_IP>:5000
```

---

### Step 6 — Start / Stop to Save Credits 💰

**Stop the instance** (pauses billing) when you don't need it:
```
AWS Console → EC2 → Instances → Select instance → Instance State → Stop
```

**Start it again** when needed:
```
AWS Console → EC2 → Instances → Select instance → Instance State → Start
```

> ⚠️ Your **Public IP changes** every time you start the instance. To get a fixed IP, allocate an **Elastic IP** (free while instance is running) from EC2 → Elastic IPs → Allocate → Associate.

---

### Step 7 — Restart App After Instance Start

Each time you start the instance again, SSH in and re-run:

```bash
ssh -i "your-key.pem" ubuntu@<NEW_PUBLIC_IP>
cd /home/ubuntu/Twitter-Sentiment-Analysis
nohup gunicorn run:app --bind 0.0.0.0:5000 > &
```

Or set up auto-start with systemd (optional but recommended):

```bash
sudo nano /etc/systemd/system/tweetsense.service
```

Paste this:

```ini
[Unit]
Description=TweetSense Flask App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/Twitter-Sentiment-Analysis
ExecStart=/usr/local/bin/gunicorn run:app --bind 0.0.0.0:5000
Restart=always

[Install]
WantedBy=multi-user.target
```

Then enable it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable tweetsense
sudo systemctl start tweetsense
```

Now the app **auto-starts every time** the EC2 instance boots.

---

## 💰 Cost Estimate

| Usage | Approx Cost |
|-------|-------------|
| t3.micro running 24/7 for 1 month | ~$7.50 |
| t3.micro running 2 hrs/day for 1 month | ~$0.60 |
| Stopping instance when not in use | $0.00/hr |
| Your $100 AWS credit | Covers ~13 months of 24/7 or years of on-demand use |

---

## 📓 Model Training

The complete training pipeline is in `Twitter.ipynb`, which covers:

1. **Data Loading** — Load Sentiment140 dataset (1.6M tweets)
2. **Exploratory Data Analysis** — Dataset shape, missing values, class distribution
3. **Text Preprocessing** — Cleaning, stemming, stopword removal
4. **Feature Extraction** — TF-IDF vectorization
5. **Model Training** — Logistic Regression classifier
6. **Evaluation** — Accuracy metrics on train/test split
7. **Model Export** — Save model & vectorizer as `.sav` files using pickle

```python
import pickle
pickle.dump(model, open('trained_model.sav', 'wb'))
pickle.dump(vectorizer, open('vectorizer.sav', 'wb'))
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

---

## 📄 License

This project is open source and available for educational purposes.

---

<p align="center">Created by <strong>Hussen Shaikh</strong></p>
