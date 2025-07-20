from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from textblob import TextBlob
from datetime import datetime
import re
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"

# User Database
users = {
    "admin": "admin123"
}

# In-Memory Feedback Storage (Replace with a database in production)
feedback_list = []

# YouTube Video Recommendations with thumbnails and titles
VIDEO_RECOMMENDATIONS = {
    "happy": {
        "main": {
            "url": "https://www.youtube.com/watch?v=T91yo5LUVRk",
            "thumbnail": "https://img.youtube.com/vi/T91yo5LUVRk/maxresdefault.jpg",
            "title": "Uplifting Music for Happy Mood"
        },
        "similar": [
            {
                "url": "https://youtu.be/BmwvpbJwJT8",
                "thumbnail": "https://img.youtube.com/vi/BmwvpbJwJT8/maxresdefault.jpg",
                "title": "Happy Short Video 1"
            },
            {
                "url": "https://youtube.com/shorts/19FuXUsO6Bg",
                "thumbnail": "https://img.youtube.com/vi/19FuXUsO6Bg/maxresdefault.jpg",
                "title": "Happy Short Video 2"
            },
            {
                "url": "https://youtube.com/shorts/0mDLv261Z-U",
                "thumbnail": "https://img.youtube.com/vi/0mDLv261Z-U/maxresdefault.jpg",
                "title": "Joyful Moment"
            },
            {
                "url": "https://youtu.be/OMygIYvrGUw",
                "thumbnail": "https://img.youtube.com/vi/OMygIYvrGUw/maxresdefault.jpg",
                "title": "Positive Vibes"
            },
            {
                "url": "https://youtube.com/shorts/oLcaXV5_V7s",
                "thumbnail": "https://img.youtube.com/vi/oLcaXV5_V7s/maxresdefault.jpg",
                "title": "Happy Short Video 3"
            },
            {
                "url": "https://www.youtube.com/shorts/Q5HQnpZEmCY",
                "thumbnail": "https://img.youtube.com/vi/Q5HQnpZEmCY/maxresdefault.jpg",
                "title": "Happy Short Video 4"
            }
        ]
    },
    "motivational": {
        "main": {
            "url": "https://www.youtube.com/watch?v=ZXsQAXx_ao0",
            "thumbnail": "https://img.youtube.com/vi/ZXsQAXx_ao0/maxresdefault.jpg",
            "title": "Powerful Motivational Speech"
        },
        "similar": [
            {
                "url": "https://www.youtube.com/watch?v=lsSC2vx7zFQ",
                "thumbnail": "https://img.youtube.com/vi/lsSC2vx7zFQ/maxresdefault.jpg",
                "title": "Never Give Up Motivation"
            },
            {
                "url": "https://www.youtube.com/watch?v=WxPApTGWwas",
                "thumbnail": "https://img.youtube.com/vi/WxPApTGWwas/maxresdefault.jpg",
                "title": "Believe in Yourself"
            },
            {
                "url": "https://www.youtube.com/watch?v=7XFLTDQ4JMk",
                "thumbnail": "https://img.youtube.com/vi/7XFLTDQ4JMk/maxresdefault.jpg",
                "title": "Daily Motivation"
            },
            {
                "url": "https://www.youtube.com/watch?v=ZXsQAXx_ao0",
                "thumbnail": "https://img.youtube.com/vi/ZXsQAXx_ao0/maxresdefault.jpg",
                "title": "Success Mindset"
            }
        ]
    },
    "sad": {
        "main": {
            "url": "https://www.youtube.com/watch?v=Xq-ljRXNtS0",
            "thumbnail": "https://img.youtube.com/vi/Xq-ljRXNtS0/maxresdefault.jpg",
            "title": "Calming Music to Overcome Sadness"
        },
        "similar": [
            {
                "url": "https://youtu.be/BmwvpbJwJT8",
                "thumbnail": "https://img.youtube.com/vi/BmwvpbJwJT8/maxresdefault.jpg",
                "title": "Sad Short Video 1"
            },
            {
                "url": "https://youtube.com/shorts/8un9wE_9PfU",
                "thumbnail": "https://img.youtube.com/vi/8un9wE_9PfU/maxresdefault.jpg",
                "title": "Comforting Content"
            },
            {
                "url": "https://youtu.be/I5_BuHWAlnw",
                "thumbnail": "https://img.youtube.com/vi/I5_BuHWAlnw/maxresdefault.jpg",
                "title": "Healing Journey"
            },
            {
                "url": "https://youtube.com/shorts/oLcaXV5_V7s",
                "thumbnail": "https://img.youtube.com/vi/oLcaXV5_V7s/maxresdefault.jpg",
                "title": "Sad Short Video 3"
            },
            {
                "url": "https://www.youtube.com/shorts/Q5HQnpZEmCY",
                "thumbnail": "https://img.youtube.com/vi/Q5HQnpZEmCY/maxresdefault.jpg",
                "title": "Sad Short Video 4"
            }
        ]
    },
    "surprised": {
        "main": {
            "url": "https://www.youtube.com/watch?v=Fz_ZUphNRlQ",
            "thumbnail": "https://img.youtube.com/vi/Fz_ZUphNRlQ/maxresdefault.jpg",
            "title": "Interesting Videos for Surprising Moments"
        },
        "similar": [
            {
                "url": "https://youtube.com/shorts/LxYy_FgSoTA",
                "thumbnail": "https://img.youtube.com/vi/LxYy_FgSoTA/maxresdefault.jpg",
                "title": "Amazing Discovery"
            },
            {
                "url": "https://youtu.be/XAL2Xf5ihzM",
                "thumbnail": "https://img.youtube.com/vi/XAL2Xf5ihzM/maxresdefault.jpg",
                "title": "Wonderful Moment"
            },
            {
                "url": "https://youtu.be/BmwvpbJwJT8",
                "thumbnail": "https://img.youtube.com/vi/BmwvpbJwJT8/maxresdefault.jpg",
                "title": "Surprised Short Video 1"
            },
            {
                "url": "https://youtube.com/shorts/19FuXUsO6Bg",
                "thumbnail": "https://img.youtube.com/vi/19FuXUsO6Bg/maxresdefault.jpg",
                "title": "Surprised Short Video 2"
            },
            {
                "url": "https://youtube.com/shorts/oLcaXV5_V7s",
                "thumbnail": "https://img.youtube.com/vi/oLcaXV5_V7s/maxresdefault.jpg",
                "title": "Surprised Short Video 3"
            },
            {
                "url": "https://www.youtube.com/shorts/Q5HQnpZEmCY",
                "thumbnail": "https://img.youtube.com/vi/Q5HQnpZEmCY/maxresdefault.jpg",
                "title": "Surprised Short Video 4"
            }
        ]
    },
    "lonely": {
        "main": {
            "url": "https://www.youtube.com/watch?v=JoaE7ZijQ84",
            "thumbnail": "https://img.youtube.com/vi/JoaE7ZijQ84/maxresdefault.jpg",
            "title": "Music for When You Feel Alone"
        },
        "similar": [
            {
                "url": "https://youtu.be/BmwvpbJwJT8",
                "thumbnail": "https://img.youtube.com/vi/BmwvpbJwJT8/maxresdefault.jpg",
                "title": "Companionship Video"
            },
            {
                "url": "https://youtube.com/shorts/19FuXUsO6Bg",
                "thumbnail": "https://img.youtube.com/vi/19FuXUsO6Bg/maxresdefault.jpg",
                "title": "Connection Video"
            },
            {
                "url": "https://youtube.com/shorts/BmGt9dBphSo",
                "thumbnail": "https://img.youtube.com/vi/BmGt9dBphSo/maxresdefault.jpg",
                "title": "Short Video 5"
            },
            {
                "url": "https://youtube.com/shorts/UWBWWKJDYH8",
                "thumbnail": "https://img.youtube.com/vi/UWBWWKJDYH8/maxresdefault.jpg",
                "title": "Short Video 6"
            },
            {
                "url": "https://youtube.com/shorts/AIcHGcU0V3g",
                "thumbnail": "https://img.youtube.com/vi/AIcHGcU0V3g/maxresdefault.jpg",
                "title": "Short Video 7"
            }
        ]
    }
}

# Emotion-specific chat responses
EMOTION_RESPONSES = {
    "sad": [
        "I notice you're feeling down. Would you like to watch some uplifting videos to help lift your spirits?",
        "It's okay to feel sad sometimes. Let's try to bring some joy into your day with these positive videos.",
        "I'm here to help you feel better. These videos might help brighten your mood.",
        "Remember, every cloud has a silver lining. Let's find some happiness in these videos."
    ],
    "angry": [
        "I understand you're feeling angry. Let's try to find some calm and peace with these soothing videos.",
        "It's natural to feel angry sometimes. These videos might help you find some relief and relaxation.",
        "Let's work on turning that anger into positive energy. These videos could help.",
        "Take a deep breath. These calming videos might help you feel better."
    ],
    "neutral": [
        "Looking for some mind-betterment videos? These might help you grow and learn.",
        "These videos could help you discover new perspectives and ideas.",
        "Want to expand your mind? Check out these thought-provoking videos.",
        "These videos might help you find new inspiration and motivation."
    ],
    "happy": [
        "Great to see you're feeling happy! Let's keep that positive energy going with these videos.",
        "Your happiness is contagious! Here are some more joyful videos to enjoy.",
        "Keep that smile going with these uplifting videos.",
        "Let's maintain that positive mood with these cheerful videos."
    ],
    "motivational": [
        "Need some motivation? Here are some powerful videos to inspire you!",
        "Let's boost your motivation with these inspiring videos.",
        "Time to get motivated! Check out these uplifting videos.",
        "Ready to be inspired? Here are some motivational videos for you."
    ]
}

def get_youtube_id(url):
    youtube_regex = r'(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(youtube_regex, url)
    return match.group(1) if match else None

@app.route('/')
def home():
    if "user" in session:
        return redirect(url_for("chatbot"))
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username in users:
        return jsonify({"message": "User already exists!"}), 400

    users[username] = password
    session["user"] = username  # Auto-login after registration
    return jsonify({"message": "User registered successfully!", "redirect": url_for("chatbot")}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if users.get(username) == password:
        session["user"] = username
        return jsonify({"message": "User login successful!", "redirect": url_for("chatbot")}), 200
    
    return jsonify({"message": "Invalid credentials!"}), 401

# Admin Login Route
@app.route('/admin', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "admin123":
        session["admin"] = username
        return jsonify({"message": "Admin login successful!", "redirect": url_for("admin_panel")}), 200

    return jsonify({"message": "Invalid admin credentials!"}), 401

# Admin Panel Route
@app.route('/admin_panel')
def admin_panel():
    if "admin" not in session:
        return redirect(url_for("home"))
    return render_template("admin.html")

# Fetch Feedback for Admin Panel
@app.route('/get-feedback', methods=['GET'])
def get_feedback():
    if "admin" not in session:
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(feedback_list), 200

@app.route('/logout')
def logout():
    session.pop("user", None)
    session.pop("admin", None)
    return redirect(url_for("home"))

@app.route('/chatbot')
def chatbot():
    if "user" not in session:
        return redirect(url_for("home"))
    return render_template("chatbot.html")

# Track shown videos in session
def get_shown_videos():
    return session.get("shown_videos", [])

def add_shown_video(video_url):
    shown_videos = get_shown_videos()
    shown_videos.append(video_url)
    session["shown_videos"] = shown_videos

def clear_shown_videos():
    session["shown_videos"] = []

# Function to get all available videos across all emotions
def get_all_available_videos():
    all_videos = []
    for emotion in VIDEO_RECOMMENDATIONS:
        emotion_videos = VIDEO_RECOMMENDATIONS[emotion]
        all_videos.append(emotion_videos["main"])
        all_videos.extend(emotion_videos["similar"])
    return all_videos

# Function to get a different video recommendation
def get_different_video(current_video_url, current_emotion="happy"):
    # Get videos only from the current emotion
    emotion_videos = VIDEO_RECOMMENDATIONS.get(current_emotion, VIDEO_RECOMMENDATIONS["happy"])
    all_videos = [emotion_videos["main"]] + emotion_videos["similar"]
    
    # Filter out the current video and previously shown videos
    shown_videos = get_shown_videos()
    available_videos = [v for v in all_videos if v["url"] not in shown_videos]
    
    if available_videos:
        selected_video = random.choice(available_videos)
        add_shown_video(selected_video["url"])
        return selected_video
    # If all videos have been shown, clear the history and start fresh
    clear_shown_videos()
    return emotion_videos["main"]

def get_emotion_response(emotion):
    responses = EMOTION_RESPONSES.get(emotion, EMOTION_RESPONSES["neutral"])
    return random.choice(responses)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").lower()
    
    # Check for motivational video request
    if any(word in user_message for word in ["motivational", "motivation", "inspire", "inspiration", "motivate"]):
        emotion = "motivational"
        emotion_videos = VIDEO_RECOMMENDATIONS.get(emotion)
        video_data = emotion_videos["main"]
        session["last_video_url"] = video_data["url"]
        session["current_emotion"] = emotion
        add_shown_video(video_data["url"])
        
        # Get all motivational videos
        all_videos = [emotion_videos["main"]] + emotion_videos["similar"]
        shown_videos = get_shown_videos()
        available_videos = [v for v in all_videos if v["url"] not in shown_videos]
        
        # If we don't have enough unique videos, clear the history
        if len(available_videos) < 3:
            clear_shown_videos()
            available_videos = all_videos
        
        # Select three random videos
        selected_similar = random.sample(available_videos, min(3, len(available_videos)))
        selected_videos = [video_data] + selected_similar
        
        # Add selected videos to shown videos
        for video in selected_similar:
            add_shown_video(video["url"])
        
        # Get emotion-specific response
        response_message = get_emotion_response(emotion)
        
        return jsonify({
            "reply": response_message,
            "showVideos": True,
            "videoSuggestions": selected_videos
        })
    
    # Check if user doesn't like the current video
    if any(phrase in user_message for phrase in ["don't like", "dislike", "not interested", "another", "different"]):
        # Get the last video URL and emotion from the session
        last_video_url = session.get("last_video_url", VIDEO_RECOMMENDATIONS["happy"]["main"]["url"])
        current_emotion = session.get("current_emotion", "happy")
        
        new_video = get_different_video(last_video_url, current_emotion)
        session["last_video_url"] = new_video["url"]
        
        # Get videos only from the current emotion
        emotion_videos = VIDEO_RECOMMENDATIONS.get(current_emotion, VIDEO_RECOMMENDATIONS["happy"])
        all_videos = [emotion_videos["main"]] + emotion_videos["similar"]
        shown_videos = get_shown_videos()
        available_videos = [v for v in all_videos if v["url"] not in shown_videos]
        
        # If we don't have enough unique videos, clear the history
        if len(available_videos) < 4:
            clear_shown_videos()
            available_videos = all_videos
        
        # Select four random videos from the current emotion
        selected_videos = random.sample(available_videos, min(4, len(available_videos)))
        
        # Add selected videos to shown videos
        for video in selected_videos:
            add_shown_video(video["url"])
        
        # Get emotion-specific response
        response_message = get_emotion_response(current_emotion)
        
        return jsonify({
            "reply": response_message,
            "showVideos": True,
            "videoSuggestions": selected_videos
        })
    
    # Analyze sentiment for emotion detection
    blob = TextBlob(user_message)
    sentiment = blob.sentiment.polarity
    
    # Map sentiment to emotion
    if sentiment > 0.3:
        emotion = "happy"
    elif sentiment < -0.3:
        emotion = "sad"
    else:
        emotion = "neutral"
    
    emotion_videos = VIDEO_RECOMMENDATIONS.get(emotion, VIDEO_RECOMMENDATIONS["happy"])
    video_data = emotion_videos["main"]
    session["last_video_url"] = video_data["url"]
    session["current_emotion"] = emotion
    add_shown_video(video_data["url"])
    
    # Get videos only from the current emotion
    all_videos = [emotion_videos["main"]] + emotion_videos["similar"]
    shown_videos = get_shown_videos()
    available_videos = [v for v in all_videos if v["url"] not in shown_videos]
    
    # If we don't have enough unique videos, clear the history
    if len(available_videos) < 3:
        clear_shown_videos()
        available_videos = all_videos
    
    # Select three random videos from the current emotion
    selected_similar = random.sample(available_videos, min(3, len(available_videos)))
    selected_videos = [video_data] + selected_similar
    
    # Add selected videos to shown videos
    for video in selected_similar:
        add_shown_video(video["url"])
    
    # Get emotion-specific response
    response_message = get_emotion_response(emotion)
    
    return jsonify({
        "reply": response_message,
        "showVideos": True,
        "videoSuggestions": selected_videos
    })

@app.route("/emotion", methods=['POST'])
def emotion_response():
    data = request.json
    emotion = data.get("emotion", "").lower()
    
    emotion_videos = VIDEO_RECOMMENDATIONS.get(emotion, VIDEO_RECOMMENDATIONS["happy"])
    video_data = emotion_videos["main"]
    session["last_video_url"] = video_data["url"]
    session["current_emotion"] = emotion
    add_shown_video(video_data["url"])
    
    # Get videos only from the current emotion
    all_videos = [emotion_videos["main"]] + emotion_videos["similar"]
    shown_videos = get_shown_videos()
    available_videos = [v for v in all_videos if v["url"] not in shown_videos]
    
    # If we don't have enough unique videos, clear the history
    if len(available_videos) < 3:
        clear_shown_videos()
        available_videos = all_videos
    
    # Select three random videos from the current emotion
    selected_similar = random.sample(available_videos, min(3, len(available_videos)))
    selected_videos = [video_data] + selected_similar
    
    # Add selected videos to shown videos
    for video in selected_similar:
        add_shown_video(video["url"])
    
    # Get emotion-specific response
    response_message = get_emotion_response(emotion)

    return jsonify({
        "reply": response_message,
        "showVideos": True,
        "videoSuggestions": selected_videos
    })

# Save Feedback
@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.get_json()
    username = session.get("user", "Guest")  # Default to Guest if not logged in
    feedback_message = data.get("message")

    if feedback_message:
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        feedback_list.append({"username": username, "message": feedback_message, "date": current_date})
        return jsonify({"message": "Thank you for your feedback!"}), 200
    return jsonify({"message": "Feedback cannot be empty!"}), 400

if __name__ == "__main__":
    app.run(debug=True)  