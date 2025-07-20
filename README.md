
# 🧠 Sentiment-Based Mental Health Chatbot System (Using Rasa Framework)

This project is a **Mental Health Chatbot** designed using the **Rasa Framework**. The system interacts with users, identifies their mental health status through sentiment analysis, and provides supportive responses or guidance accordingly.

## 💡 Objective

To build a smart, AI-powered chatbot that:
- Understands user messages
- Detects emotional tone or mental state
- Responds empathetically or routes them to mental health support

## ⚙️ Technologies Used

- **NLP Framework:** Rasa (NLU + Core)
- **Language:** Python
- **Front-end (if any):** HTML/CSS/JS or React (optional)
- **Libraries:** spaCy, sklearn, pandas
- **Deployment:** Localhost / Docker / Web-based client

## 📁 Project Structure

```
Mental-Health-Chatbot/
│
├── data/                   # Training data (NLU, stories)
├── models/                 # Trained Rasa models
├── actions/                # Custom Python actions
├── domain.yml              # Intents, entities, responses
├── config.yml              # Rasa pipeline and policies
├── credentials.yml         # Channels and credentials
├── endpoints.yml           # Action server endpoints
├── README.md               # Project documentation
```

## 🧪 How to Run

### 1. Clone the Repo

```bash
git clone https://github.com/DhakshanaMohan/Sentiment-Based-Mental-Health-Chatbot-System-Using-Rasa-Framework.git
cd Sentiment-Based-Mental-Health-Chatbot-System-Using-Rasa-Framework
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate    # On Windows
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Train the Model

```bash
rasa train
```

### 5. Run Rasa Actions Server

```bash
rasa run actions
```

### 6. Run the Chatbot

```bash
rasa shell
```

> Optionally, you can run it in interactive mode using `rasa interactive`.

## 🧠 Features

- Detects user sentiment via trained NLU model
- Provides responses tailored to stress, anxiety, or low mood
- Supports customizable stories, actions, and responses
- Can be integrated with UI or voice platforms

## 📸 Screenshots

<img width="696" height="392" alt="image" src="https://github.com/user-attachments/assets/67004905-4262-472c-909d-94de659f2889" />
<img width="744" height="418" alt="image" src="https://github.com/user-attachments/assets/9f0be3d2-7eda-4a2b-b637-0136af5cb3da" />
<img width="766" height="431" alt="image" src="https://github.com/user-attachments/assets/7fb8e5b1-4a70-43c9-8051-b0f2f69841b7" />
<img width="826" height="464" alt="image" src="https://github.com/user-attachments/assets/efc17db7-a759-493d-9c10-2d5110b85b64" />
<img width="827" height="465" alt="image" src="https://github.com/user-attachments/assets/298ece0e-46c3-4ec3-bdde-89e38ac03b5e" />

## 🙋‍♀️ Developed By

**Dhakshana M**  
B.Tech Information Technology,  
M. Kumarasamy College of Engineering

## 📬 Contact

- GitHub: [DhakshanaMohan](https://github.com/DhakshanaMohan)
- Email: *dhakshana2103@gmail.com*

