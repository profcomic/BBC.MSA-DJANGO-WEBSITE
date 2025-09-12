# Berean Bible Church Mombasa Website

## Tech Stack
- Django (Python)
- HTML
- CSS (Tailwind CSS)
- SQLite (default for development)

## Getting Started

1. **Clone the repository:**
    ```bash
    git clone https://github.com/profcomic/BBC.MSA-DJANGO-WEBSITE.git
    cd BBC.MSA-DJANGO-WEBSITE
    ```

2. **Install dependencies:**
    ```bash
    pip install django
    ```

3. **Run migrations and start the server:**
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

4. **Open in your browser:**  
    [http://localhost:8000/](http://localhost:8000/)

## Project Structure

- `BBCMAINWEBSITE/` - Django project configuration
- `mainapp/` - Main app (templates, static files)
- `mainapp/templates/mainapp/` - HTML templates
- `mainapp/static/` - CSS, images, static assets

## Contributing

Contributions are welcome! To contribute:

1. Fork this repository.
2. Create your feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

© 2025 Berean Bible Church Mombasa. All rights reserved.
