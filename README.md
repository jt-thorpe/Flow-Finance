# Flow Finance

Flow Finance is a modern personal finance management application that helps users track their income, expenses, and budgets with an intuitive interface. Built with a robust tech stack combining Python Flask backend and Next.js frontend, it offers a secure and efficient way to manage personal finances.

## 🌟 Features

- **Secure Authentication**
  - JWT-based authentication system
  - Protected routes and API endpoints
  - Secure password handling

- **Transaction Management**
  - Track income and expenses
  - Support for recurring transactions
  - Categorisation of transactions
  - Transaction history and filtering

- **Budget Tracking**
  - Set budget goals by category
  - Track spending against budgets
  - Visual budget progress indicators
  - Monthly and yearly budget views

- **Interactive Dashboard**
  - Real-time financial overview
  - Income vs. expenses visualisation
  - Budget summary with progress bars
  - Recent transactions list
  - Responsive design for all devices

- **Technical Features**
  - RESTful API architecture
  - PostgreSQL database with SQLAlchemy ORM
  - Docker containerisation
  - TypeScript for type safety
  - Tailwind CSS for styling
  - Responsive design

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js (v18 or higher)
- Python 3.8 or higher
- PostgreSQL

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/jt-thorpe/Flow-Finance.git
   cd Flow-Finance
   ```

2. Set up environment variables:
   - Copy `.env.example` to `.env` in both frontend and backend directories
   - Update the variables with your configuration

3. Generate SSL certificates (required for HTTPS):
   ```bash
   # Install mkcert
   # On macOS:
   brew install mkcert
   # On Linux:
   sudo apt install mkcert
   # On Windows:
   choco install mkcert

   # Generate certificates
   cd frontend/certificates
   mkcert -install
   mkcert localhost
   ```

4. Start the application using Docker:
   ```bash
   docker-compose up --build
   ```

   Frontend:
   ```bash
   cd frontend
   npm install
   npm run https-dev
   ```

5. Access the application:
   - Frontend: https://localhost:3000
   - Backend API: http://localhost:5000

## 🛠️ Development

### Project Structure

```
Flow-Finance/
├── backend/
│   ├── backend/
│   │   ├── routes/         # API endpoints and route handlers
│   │   ├── models/         # Database models and schemas
│   │   ├── services/       # Business logic and service layer
│   │   ├── queries/        # Database queries and operations
│   │   ├── enums/          # Enumeration types and constants
│   │   ├── extensions.py   # Flask extensions configuration
│   │   ├── app.py         # Main application entry point
│   │   └── utils.py       # Utility functions and helpers
│   ├── tests/             # Backend test suite
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Backend container configuration
├── frontend/
│   ├── app/               # Next.js app directory (pages and layouts)
│   ├── components/        # Reusable UI components
│   ├── services/          # API service functions
│   ├── types/            # TypeScript type definitions
│   ├── context/          # React context providers
│   ├── hooks/            # Custom React hooks
│   ├── lib/              # Utility functions and shared code
│   ├── styles/           # Global styles and Tailwind config
│   ├── config/           # Application configuration
│   └── certificates/     # Directory for SSL certificates (generate with mkcert)
└── docker/              # Docker configuration files
```

### Running Tests

Backend:
```bash
cd backend
pytest
```

<!-- Frontend:
```bash
cd frontend
npm test
``` -->

## 🔒 Security

- JWT-based authentication
- HTTPS support
- Secure password hashing
- Protected API endpoints
- Environment variable configuration

## 🤝 Contributing

This project is currently a work in progress and not open for contributions. However, feel free to:
- Star the repository
- Fork for personal use
- Report issues
- Suggest improvements

## 📝 License

This project is proprietary and not licensed for public use.

## 👤 Author

**Jake Thorpe**
- 💬 Contact: jtt-applications@proton.me
- 🔗 GitHub: [github.com/jt-thorpe](https://github.com/jt-thorpe/)
- 🔗 LinkedIn: [linkedin.com/in/jt-thorpe](https://www.linkedin.com/in/jt-thorpe/)
- 🌐 Portfolio: Coming soon

## ⭐ Support

If you find this project helpful, please give it a star on GitHub!

