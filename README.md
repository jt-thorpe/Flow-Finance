# Flow-Finance

Flow-Finance is a **personal finance budgeting application** designed to help users **track income, expenses, and budgets** efficiently. Built with **Python + Flask (backend) & TypeScript + Next.js (frontend)**, the app provides a seamless experience for managing personal finances.

## Features

✅ **User Authentication** – Secure JWT-based login system.\
✅ **Transaction Management** – Track income, expenses, and recurring transactions.\
✅ **Budget Tracking** – Set and monitor budget goals.\
✅ **Interactive Dashboard** – Visual representation of finances.\
✅ **Dockerized Setup** – Easily deployable with `docker-compose`.\
✅ **Optimized Database Structure** – Uses PostgreSQL with SQLAlchemy ORM.

---

## Project Structure

```
Flow-Finance/
├── backend/            # Backend (Python - Flask)
│   ├── backend/        # Python module
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── extensions.py
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── queries/
│   │   ├── enums/
│   │
│   ├── scripts/        # Database setup & utility scripts
│   ├── migrations/     # Alembic migrations (coming soon)
│   ├── tests/          # Unit tests for backend
│   ├── .env            # Environment variables
│   ├── Dockerfile      # Backend Dockerfile
│   ├── requirements.txt
│
├── frontend/           # Frontend (Next.js - TypeScript)
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── next.config.js
│   ├── tsconfig.json
│   ├── .env.local
│
├── docker/             # Docker-related scripts (optional)
│   ├── start.sh
│   ├── cleanup.sh
│
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── README.md
```

---

## 🚀 Getting Started

### **🔹 Prerequisites**

Make sure you have the following installed:

- **Docker** & **Docker Compose**
- **Python 3.12+**
- **Node.js (for frontend)**

---

### **🔹 Backend Setup (Flask API)**

1. **Clone the repository:**

```sh
git clone https://github.com/yourusername/Flow-Finance.git
cd Flow-Finance
```

2. **Create a virtual environment:**

```sh
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```sh
pip install -r requirements.txt
```

4. **Setup environment variables (****`.env`**** in backend/):**

```ini
JWT_SECRET_KEY=your_jwt_secret
FLOW_DB_URI=postgresql://user:password@host:port/database
FLASK_SECRET_KEY=your_flask_secret
REDIS_HOST=redis
```

5. **Run the backend server:**

```sh
python -m backend.app
```

✅ API will run at `http://localhost:5000/`.

---

### **🔹 Frontend Setup (Next.js)**

1. **Go to frontend directory:**

```sh
cd frontend
```

2. **Install dependencies:**

```sh
npm install
```

3. **Run the development server:**

```sh
npm run dev
```

✅ Frontend will be available at `http://localhost:3000/`.

---

## Running with Docker

### **🔹 One-Step Setup**

To run the **backend and Redis** using Docker:

```sh
docker compose up --build
```

✅ **Backend will be running at** `http://localhost:5000/`\
✅ **Redis will be running on port** `6379`

---

## Development Status

Flow-Finance is **a work in progress** and **not yet complete**. The application is intended as a **portfolio piece** to showcase development skills and **eventually serve a small set of users**. Contributions are not currently open but may be considered in the future.

---

## License

This project is licensed under **[Your Name]**'s proprietary license. All rights reserved.

---

## To-Do / Roadmap

- ✅ Implement user authentication
- ✅ Improve database performance
- 🛠 Add analytics dashboard
- 🛠 Write unit tests for backend services
- 🛠 Deploy using CI/CD

---

## Credits & Contact

Developed by **Jake Thorpe**\
💬 Contact: jtt-applications@proton.me\
🔗 GitHub: @jt-thorpe\
🔗 Portfolio: coming soon

---

## Support the Project

If you like this project, give it a ⭐ on GitHub!

