# 🐱 Meow - Cat Community Platform

<div align="center">

**A Beautiful Community Platform for Cat Lovers**

*Featuring Social Sharing, Smart Veterinary Chatbot, and Real-time Vet Clinic Finder*

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web_Framework-black?logo=flask)](https://flask.palletsprojects.com/)
[![SQL Server](https://img.shields.io/badge/SQL_Server-Database-red?logo=microsoft-sql-server)](https://www.microsoft.com/sql-server)
[![JavaScript](https://img.shields.io/badge/JavaScript-Vanilla-yellow?logo=javascript)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

</div>

---

## 📚 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Technology Stack](#%EF%B8%8F-technology-stack)
- [System Components](#-system-components)
- [Usage Guide](#-usage-guide)
- [Project Structure](#-project-structure)
- [Screenshots](#%EF%B8%8F-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**Meow** is a comprehensive web platform designed for cat enthusiasts to share experiences, seek expert advice, and access veterinary resources. Built with a modern web architecture, it provides a seamless experience for cat lovers to connect, learn, and find help.

### Key Capabilities

- 👥 **Community Forum** - Share cat stories and connect with other cat lovers
- 🤖 **AI Chatbot** - RAG-based veterinary assistant for health advice
- 🏥 **Vet Finder** - Real-time Google Maps scraping for nearby clinics
- 🌐 **Bilingual Support** - Full English and Arabic language support
- 📱 **Mobile-First** - Responsive design that works on all devices
- 💬 **Interactive Features** - Emoji reactions, threaded comments, and more

---

## ✨ Features

### 🏠 Home Section
Welcome page featuring:
- **Cat-Themed Visuals** - Beautiful, welcoming design
- **Quick Navigation** - Easy access to all features
- **CTA Buttons** - Signup, login, and chat prompts

### 👥 Community Forum
Share and connect with other cat lovers:
- **Create & Share** - Post your cat stories and experiences
- **React with Emojis** - Express your feelings with emoji reactions
- **Threaded Comments** - Reply and engage in discussions
- **Reverse Chronological Feed** - Newest posts appear first
- **Auth-Protected Posting** - Sign up required to post

### 🤖 Cat Assistant Chatbot
Get expert advice on cat health and care:
- **RAG-Based AI** - Uses veterinary sources for accurate answers
- **Bilingual Support** - Available in English & Arabic
- **Chat History** - Review previous conversations
- **Cute Pastel Interface** - User-friendly design
- **Backup AI Models** - Ensures availability

**Example Questions:**
- "Why is my cat not eating?"
- "How often should I take my cat to the vet?"
- "What are signs of a sick cat?"

### 🏥 Veterinary Clinic Search
Find veterinary clinics in your area:
- **Real-Time Scraping** - Pulls data directly from Google Maps
- **Detailed Information** - Shows rating, address, website, phone, and hours
- **Comprehensive Results** - Loads up to 30 clinics
- **Built with Selenium** - Reliable web scraping technology

---

## 🛠️ Technology Stack

### Frontend
- **HTML5** - Semantic page structure
- **CSS3** - Pastel, responsive design with mobile-first approach
- **Vanilla JavaScript** - Interactive features without framework overhead

### Backend & Processing
- **Python 3** - Core language
- **Flask** - Lightweight web framework
- **Flask-CORS** - Cross-origin resource sharing
- **Flask-SQLAlchemy** - Database ORM
- **Selenium** - Web scraping for clinic data
- **LangChain + FAISS** - RAG-based chatbot intelligence

### Database
- **SQL Server** - Primary database for users, posts, and comments

### External APIs
- **Random User API** - Generates profile avatars
- **Google Maps** - Provides clinic information
- **GPT-4o-mini** - AI language model with backup options
- **File Handlers** - PyPDF2, python-pptx for document processing

---

## 🧩 System Components

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | HTML5, CSS3, JavaScript | User interface and interactions |
| **Web Server** | Flask | API endpoints and routing |
| **Database** | SQL Server | User data, posts, comments storage |
| **Chatbot Engine** | LangChain, FAISS | RAG-based veterinary assistance |
| **Vet Finder** | Selenium, Google Maps | Real-time clinic data scraping |
| **Authentication** | Flask sessions | User login and security |
| **AI Processing** | GPT-4o-mini | Natural language understanding |

---

## 📘 Usage Guide

### ✨ Creating an Account

1. **Navigate to Signup**
   - Click the "Sign Up" button on the home page

2. **Enter Your Details**
   - Fill in name, email, and password
   - Optionally upload a profile picture

3. **Submit**
   - Click submit to create your account
   - You'll be automatically logged in

### ✨ Logging In

1. **Click "Log In"**
   - Enter your registered email
   - Enter your password
   - Click "Log In" button

### ✨ Posting in Community

1. **Navigate to Community Section**
   - Click on "Community" in the navigation menu

2. **Create Your Post**
   - Type your cat story in the text box
   - Add any details about your experience

3. **Share**
   - Click "Post" button
   - Your story appears at the top of the feed 🎉

### ✨ Interacting with Posts

- **React** - Express yourself with emoji reactions
- **Comment** - Click 💬 to add your thoughts and engage in discussions
- **Read** - Browse stories from other cat lovers

### ✨ Using the Chatbot

1. **Access the Chatbot**
   - Click on "Chat" or "Cat Assistant" in the navigation

2. **Ask Your Question**
   - Type your question about cat health, behavior, or care
   - Press Enter or click Send

3. **Get Answers**
   - Receive instant, context-aware responses
   - Available in both English and Arabic

### ✨ Vet Search

1. **Open Vet Finder**
   - Navigate to the Vet Finder section

2. **Enter Location**
   - Type your city, address, or location

3. **Browse Results**
   - Click Search to load clinics
   - Scroll through up to 30 results
   - View detailed information for each clinic

---

## 📁 Project Structure

```
Cat-Community-Platform/
│
├── app.ipynb                       # Main Jupyter notebook application
├── community.db                    # SQLite database file
├── core.py                         # Core functionality and utilities
├── database.py                     # Database connection and operations
├── models.py                       # Database models (User, Post, Comment)
├── vet.py                          # Veterinary clinic finder (Selenium scraper)
├── requirements.txt                # Python dependencies

```

### File Details

| File | Purpose |
|------|---------|
| **app.ipynb** | Main application notebook with Flask server and routes |
| **community.db** | SQLite database storing users, posts, comments, and reactions |
| **core.py** | Core utilities and helper functions |
| **database.py** | Database initialization, connections, and query functions |
| **models.py** | SQLAlchemy models for User, Post, Comment tables |
| **vet.py** | Google Maps scraper for veterinary clinic search |
| **requirements.txt** | List of required Python packages |

---

## 🖼️ Screenshots

### Home Section
![Home Section](https://github.com/AlaaAhmed2221/Cat-lover-Project/blob/main/Screenshot%202025-11-25%20220708.png?raw=true)

### Community Forum
![Community Forum 1](https://github.com/AlaaAhmed2221/Cat-lover-Project/blob/main/Screenshot%202025-11-25%20220900.png?raw=true)

![Community Forum 2](https://github.com/AlaaAhmed2221/Cat-lover-Project/blob/main/Screenshot%202025-11-25%20220940.png?raw=true)

![Community Forum 3](https://github.com/AlaaAhmed2221/Cat-lover-Project/blob/main/Screenshot%202025-11-25%20221001.png?raw=true)

### Cat Assistant Chatbot
![Chatbot Interface](https://github.com/AlaaAhmed2221/Cat-lover-Project/blob/main/Screenshot%202025-11-25%20220835.png?raw=true)

### Veterinary Clinic Search
![Vet Search 1](https://github.com/AlaaAhmed2221/Cat-lover-Project/blob/main/Screenshot%202025-11-25%20221025.png?raw=true)

![Vet Search 2](https://github.com/AlaaAhmed2221/Cat-lover-Project/blob/main/Screenshot%202025-11-25%20221125.png?raw=true)

---

## 🤝 Contributing

We'd love your help to make Meow even better!

### How to Contribute

1. **Fork the Repository**
   ```bash
   git clone https://github.com/yourusername/meow-platform.git
   cd meow-platform
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**
   - Write clean, well-documented code
   - Follow existing code style
   - Test thoroughly

4. **Submit Pull Request**
   - Update documentation if needed
   - Describe your changes clearly
   - Reference any related issues

We welcome all contributions that improve the platform for cat lovers!

---

## 📄 License

This project is licensed under the **MIT License**.

You're free to use, modify, and distribute this project as long as you include the original license.

---

## 🙏 Acknowledgments

- **Community Contributors** - All the cat lovers who share their stories
- **Veterinary Experts** - For providing reliable health information
- **Open Source Community** - Flask, LangChain, Selenium, and more
- **API Providers** - Random User API, Google Maps, OpenAI

---

<div align="center">

**🐾 Enjoy Meow – Happy Cat Parenting! 🐾**

*Connecting Cat Lovers • Meow Platform*

</div>
