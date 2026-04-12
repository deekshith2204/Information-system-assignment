# About THE APP
Babla Cars is a full-stack ridesharing application created to facilitate the creation of rides, trip discovery and booking management in one integrated system. Using the application, one can be able to create an account, authenticate and make trips as a driver, find accessible rides as a passenger as well as handle their bookings in the app with a clean and organized interface. It is developed to be an academic Information Systems project although the architecture and deployment patterns are those found in actual web applications.

# TECHNOLOGIES USED
The platform is developed with a current client-server framework. The frontend is created using React and offers the interface that the user can interact with to navigate, search trips, do any booking activity, and any action involving an account. The back-end is written in FastAPI and provides RESTful API endpoints to manage authentication, trip management, and booking. The data is stored as PostgreSQL that offers a good level of persistence and scaling of application records like users, trips and Azure App Service is used for deployment. GitHub Actions is used to automate the build and deployment process.


# Frontend
React is used for frontend to build a responsive and component-driven user experience, whereas React Router takes care of navigation between the various pages of the application. The Axios is used to access the backend API enabling the frontend to receive and send data in a well-structured and efficient format. Its frontend is ready to be deployed to production, by creating a build folder and serving it with a lightweight Node.js server.

- Steps to run frontend locally
To run the frontend locally, the required dependencies can be installed using Node.js.To run execute the following commads.

1.cd frontend

2.npm install

3.npm start

After running the above commands open: http://localhost:8080

# Backend
FastAPI is used for API development at the backend with an easily understandable and maintainable structure. SQLAlchemy also provides database interaction, with application models easily mapping to PostgreSQL tables. Pydantic is a request and response validation tool to aid in making sure that data processing is consistent and secure. To deploy it, both Gunicorn and Uvicorn are deployed in tandem to execute the FastAPI application in a production-ready setup.

-Steps to run backend locally

To run the backend locally, a Python virtual environment should be created and activated before installing the required packages listed in `requirements.txt`.

1.cd backend

2.py -3.12 -m venv .venv

3..\.venv\Scripts\Activate.ps1

4.python -m pip install --upgrade pip

5.pip install -r requirements.txt

6.uvicorn app.main:app --reload

Once the backend is running, the API documentation is available at: /http://localhost:8000/docs

# Links

The Babla Cars application is available online through Azure App Service.

Frontend application: [Open Babla Cars](https://rideshare-frontend.azurewebsites.net)

Backend API: [Open Backend API](https://rideshare-api-dmanbedkcvhbfqbh.italynorth-01.azurewebsites.net)

API documentation: [View Swagger Docs](https://rideshare-api-dmanbedkcvhbfqbh.italynorth-01.azurewebsites.net/docs)

