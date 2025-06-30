# 🌾 AgriShop - Farmer Online Selling Application

AgriShop is an innovative web-based platform that empowers farmers to sell their agricultural products directly to consumers. It bridges the gap between rural producers and urban buyers, enabling a transparent, fair, and accessible online marketplace.

## 🚀 Features

- 🧑‍🌾 **Farmer Dashboard**
  - Upload products with detailed descriptions
  - Add multiple product images
  - Edit or delete existing listings

- 🛒 **Buyer Interface**
  - Browse available products
  - Responsive product cards with pricing and offers
  - 'Request' or 'Buy Now' buttons for easy ordering

- 📦 **Offers Section**
  - Highlighted products with discounts
  - Horizontal product sliders for special deals

- 🎨 **Modern UI**
  - Built using Bootstrap 5 and custom CSS
  - Clean, mobile-friendly design with custom color palette

## 🛠️ Tech Stack

| Frontend | Backend | Database | Tools |
|----------|---------|----------|-------|
| HTML, CSS, JavaScript, Bootstrap 5 | Django (Python) | MySQL | Git, VS Code, Chrome DevTools |

## 🎨 Color Palette

- Morning Dew – `#F6FEF9`
- Fresh Sprout – `#83C441`
- Harvest – `#003023`

## 📂 Project Structure

```
AgriShop/
├── agri_shop/           # Django main project folder
├── products/            # Django app for product models & views
├── templates/
│   ├── base.html
│   ├── index.html       # Landing page
│   ├── dcard.html       # Dynamic product cards
│   └── offercard.html   # Offers section cards
├── static/
│   ├── css/
│   └── images/
├── db.sqlite3 / MySQL
└── manage.py
```

## 🧑‍💻 How to Run Locally

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/AgriShop.git
   cd AgriShop
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations and start server:**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

5. **Visit:**
   ```
   http://127.0.0.1:8000/
   ```

## 📷 Screenshots

> Add screenshots of your homepage, product cards, dashboard, and offers section here.

## ✅ Future Improvements

- ✅ User authentication system (login/signup for buyers & farmers)
- ✅ Payment gateway integration
- ✅ Product filters (by price, category)
- ✅ Order history and invoice system

## 📌 Authors

- Aniruddhya Goswami
- Ansh Soni
- Soukat Dey
- Utpal Mandal

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### 🌱 Made with ❤️ to empower farmers!
