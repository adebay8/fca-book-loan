## Project Structure

- `backend/` — Django REST API (Python)
- `frontend/` — React app (JavaScript)

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker (optional, for containerized setup)

---

### Running with Docker Compose

You can run the entire project (backend and frontend) using Docker Compose. It's recommended way to get started quickly.

1. **Build and start the containers:**
   ```sh
   docker-compose up --build
   ```
   This will build the backend and frontend images and start both services.

2. **Access the applications:**
   - Backend API: [http://localhost:8000/](http://localhost:8000/)
   - Frontend app: [http://localhost:5173/](http://localhost:5173/)


---

### Backend Setup

1. **Install dependencies:**
   ```sh
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```
3. **Run the backend server:**
   ```sh
   python manage.py runserver
   ```
   The API will be available at `http://localhost:8000/`.

---

### Frontend Setup

1. **Install dependencies:**
   ```sh
   cd frontend
   npm install
   ```
2. **Run the frontend dev server:**
   ```sh
   npm run dev
   ```
   The app will be available at `http://localhost:5173/`.
4. **Create a `.env` file:**

    In the `frontend` directory, create a file named `.env` and add the following line:

    ```
    VITE_BACKEND_URL=http://localhost:8000
    ```

    This variable sets the backend API URL for the frontend app.

---

### Database schema

![Image](https://github.com/user-attachments/assets/c2a4e5d6-8660-417f-b34d-5682f15638e8)

---


### Sample Data & User Accounts

Once the backend app is running, you can load sample books into the database using the following management command:
> **Note:** If you are running the project with Docker Compose, you need to execute management commands inside the backend container. For example:
>
> ```sh
> docker-compose exec backend python manage.py load_books
> ```

```sh
python manage.py load_books
```

To create user accounts for interacting with the app, run:

```sh
python manage.py seed_users
```

The following user accounts will be created:

| Username   | Password   | Role         |
|------------|------------|--------------|
| john      | password123  | Regular User |
| jane  | password123  | Staff/Admin  |

The `jane` account can be used for managing rentals and accessing admin-only endpoints.

---

## API Documentation

### Authentication
- Obtain JWT token:
  - **POST** `/token/`
  - Body: `{ "username": "<username>", "password": "<password>" }`
After obtaining the JWT token, include it in the `Authorization` header as follows for all authenticated requests:

```
Authorization: Bearer <your_token_here>
```

### Catalog Endpoints

- **GET** `/catalog/books/` — List all books
- **GET** `/catalog/books/<id>/` — Get book details
- **GET** `/catalog/books/<book_id>/items/` — List book items (copies)
- **GET** `/catalog/wishlist/` — Get current user's wishlist (auth required)
- **POST** `/catalog/wishlist/add/<book_id>/` — Add book to wishlist (auth required)
- **POST** `/catalog/wishlist/remove/<book_id>/` — Remove book from wishlist (auth required)

### Rentals Endpoints (Admin only)

- **POST** `/rentals/borrow/<item_id>/` — Borrow a book item
- **POST** `/rentals/return/<item_id>/` — Return a book item
- **GET** `/rentals/report/active-rentals/` — Get active rentals report

#### Example: Borrow a Book Item
- **POST** `/rentals/borrow/1/`
- Headers: `Authorization: Bearer <JWT>`

#### Example: Add to Wishlist
- **POST** `/catalog/wishlist/add/1/`
- Headers: `Authorization: Bearer <JWT>`

---

## Notes
- CORS is enabled for `http://localhost:5173`.
- For full API details, see the code in `backend/catalog/urls.py` and `backend/rentals/urls.py`.

---
