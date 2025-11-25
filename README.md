Meow - Cat Community Platform 🐱
Welcome to Meow, a purr-fect web platform for cat lovers! This community hub combines social sharing, expert veterinary advice via a smart chatbot, and real-time veterinary clinic searches. Built with love for felines, Meow helps cat owners connect, learn, and care for their furry friends in one seamless interface.
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/d72482cd-4f91-46c2-b324-9d57bfcc2f8b" />

Table of Contents
Project Overview
Features
Tech Stack
Usage Guide
Contributing
License

Project Overview
Meow is a comprehensive web platform designed for cat enthusiasts to share experiences, seek expert advice, and access veterinary resources. It integrates a community forum for storytelling, a RAG-based chatbot for veterinary queries, and a Google Maps scraper for finding nearby vets.
Purpose
Meow aims to create a centralized hub where cat lovers can:

Share heartwarming stories and tips with fellow enthusiasts 🐾
Build a supportive community focused on feline care and well-being
Access reliable veterinary information and local clinic details effortlessly

Target Users

Cat owners seeking advice, support, and connections
Pet care enthusiasts eager to share their experiences
New cat parents needing guidance on health, toxins, and daily care

Features
Meow packs a variety of cat-tastic features to enhance your experience!
🏠 Home Section

Engaging introduction with feature highlights and cat-themed visuals
Quick navigation links to community, chatbot, and vet search
Call-to-action buttons to sign up, log in, or start chatting

👥 Community Forum
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/4a0bc9a9-7c63-4950-8983-94f9fc9a12aa" />



Create and share posts about your cat adventures 📝
View posts in reverse chronological order (newest first) for fresh content
React to posts with likes and dynamic count updates ❤️
Comment on posts with nested threads for deeper discussions
User avatars with profile pictures for a personal touch
Authentication required to post, ensuring a safe space

🤖 Cat Assistant Chatbot
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/23078bc3-49c5-47a3-9373-b08ecb0ac662" />


AI-powered assistant providing helpful responses to cat-related queries
Uses Retrieval-Augmented Generation (RAG) with veterinary data sources (e.g., books on toxicology and pharmacy)
Supports natural language in English or Arabic, responding in the query's language
Maintains chat history for contextual conversations
Themed interface with pastel colors and cat logos for a fun vibe
Fallback to alternative AI models if needed (e.g., OpenRouter or Hugging Face)

🏥 Veterinary Clinic Search
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/f4621cb4-51f8-493e-9f82-1583bd4044aa" />

Search for real veterinary clinics by location using Google Maps
Scrapes details like name, rating, reviews, address, phone, hours, and website
Loads up to 30 results with scrolling for more options
Built with Selenium for reliable web scraping.
This code sets up a headless Chrome browser, searches Google Maps, scrolls for more results, and extracts clinic info using CSS selectors and regex for robustness.
Tech Stack
Meow is built with modern, efficient technologies for a smooth experience.

Frontend

HTML5: Semantic markup for accessibility
CSS3: Responsive design with media queries and pastel themes
JavaScript (Vanilla): DOM manipulation and API interactions
Responsive Design: Mobile-first approach for on-the-go cat lovers 📱

Backend

Python 3: Server-side logic and scripting
Flask: Lightweight web framework for routing and API handling
Flask-CORS: Cross-Origin Resource Sharing for secure frontend-backend communication
Flask-SQLAlchemy: ORM for database operations
Werkzeug: Security utilities like password hashing
Selenium: For veterinary clinic scraping in vet.py
LangChain & FAISS: For RAG in the chatbot, with Hugging Face embeddings

Database

SQL Server: Primary relational database for user data and posts

External APIs & Libraries

Random User API: Generates user profiles and avatars
Google Maps (via Scraper): Real-time vet clinic data
AI Models: OpenAI GPT-4o-mini for chatbot responses, with fallbacks
File Handlers: PyPDF2, python-pptx for processing veterinary documents


Usage Guide
Creating an Account

Click "Sign Up" in the navigation.
Enter your first name, last name, email, and password.
Optionally upload a profile picture 🐈.
Click "Sign Up" to join the community!

Logging In

Click "Login".
Enter your email and password.
Click "Login".
You'll see "Sign Out" once authenticated.

Posting in the Community

Go to the "Community" section.
Log in if needed.
Type your cat story in the input field.
Click "Post".
Watch it appear at the top of the feed! 🎉

Interacting with Posts

Like: Click the ❤️ icon to show love.
Comment: Click the 💬 icon to open the section.
Add Comment: Type your thoughts and click "Comment".

Using the Chatbot

Navigate to the chatbot section.
Ask questions like "What toxins harm cats?" in English or Arabic.
Get context-aware responses based on veterinary sources.
View your chat history for ongoing conversations.

Searching Vets

Enter a location (e.g., "New York") in the search bar.
The scraper fetches clinics with details like ratings and contacts.
Browse up to 30 results for the best options nearby.

Contributing
We'd love your help to make Meow even better! Fork the repo, create a branch, and submit a pull request. Follow these guidelines:

Keep code clean and cat-friendly 😺.
Test features thoroughly.
Update documentation as needed.

For issues or ideas, open a GitHub issue.
License
This project is licensed under the MIT License - see the LICENSE file for details.
Enjoy Meow and happy cat parenting! 🐾 If you have questions, reach out in the community forum.
Using the Chatbot

Navigate to the chatbot section.
Ask questions like "What toxins harm cats?" in English or Arabic.
Get context-aware responses based on veterinary sources.
View your chat history for ongoing conversations.

Searching Vets

Enter a location (e.g., "New York") in the search bar.
The scraper fetches clinics with details like ratings and contacts.
Browse up to 30 results for the best options nearby.

Contributing
We'd love your help to make Meow even better! Fork the repo, create a branch, and submit a pull request. Follow these guidelines:

Keep code clean and cat-friendly 😺.
Test features thoroughly.
Update documentation as needed.

For issues or ideas, open a GitHub issue.
License
This project is licensed under the MIT License - see the LICENSE file for details.
Enjoy Meow and happy cat parenting! 🐾 If you have questions, reach out in the community forum.
