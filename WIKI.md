# 📖 AgriShop Wiki

Welcome to the **AgriShop Wiki**! This document provides detailed information about the project's architecture, features, and database models.

## 🌟 Project Overview

**AgriShop** is a comprehensive e-commerce platform designed to bridge the gap between farmers and consumers. It allows farmers to list their produce directly on the platform, ensuring better prices and transparency. Consumers can browse fresh produce, view details, and place orders seamlessly.

## 🚀 Detailed Features

### 🧑‍🌾 For Farmers (Sellers)
- **Product Management:** Farmers can upload products with images, descriptions, units of measurement (kg, liters, etc.), and pricing.
- **Inventory Control:** Manage stock levels. Products are automatically marked as "out of stock" or "limited availability" based on quantity.
- **Dashboard:** A personal dashboard to track listed products and sales.

### 🛒 For Buyers (Consumers)
- **Browse & Search:** Easy navigation through categories and subcategories.
- **Product Details:** Detailed view of products including origin, unit price, and availability.
- **Cart & Orders:** Add items to cart and place orders.
- **Responsive Design:** Optimized for mobile and desktop viewing.

### 🔧 For Admins
- **Content Management:** Manage sliders, recommendations, and special sections (e.g., Offers, Seasonal Products) via the Django Admin panel.
- **Order Oversight:** Monitor orders and user activities.

## 🗄️ Database Models

The project uses a relational database with the following key models:

### Product & Categories
- **`Catagoriesofitems` & `SubCatagoriesofitems`:** Organize products into a hierarchy.
- **`CardDetails`:** The core product model containing:
  - Images (up to 4)
  - Price, Discount, and Final Price calculation
  - Unit of Measurement (kg, g, l, ml, etc.)
  - Availability logic
- **`ProductsOfthisWeb`:** Used for handling product submissions that might need approval (status: pending, accepted, rejected).

### Users & Profiles
- **`UserProfile`:** Extends the standard Django User to add phone, address, and company details.
- **`SellerProfile`:** specific details for sellers like brand name, category (Manufacturer/Distributor), and contact info.

### Orders
- **`Order`:** Tracks the overall order for a user, including total price and status.
- **`OrderItem`:** Links products to orders with quantity and price at the time of purchase.
- **`orderplacedfinal`:** Stores finalized order details for processing.

### Admin Managed Sections
These models control the dynamic content on the homepage:
- **`Slidermaintain`:** Homepage carousel images.
- **`Recomendations`**, **`OffersSection`**, **`GrowthSection`**, **`SmartfarmingSection`**, **`SpraySection`**, **`SeedsSection`**, **`SeasonalSection`**: various curated lists of products displayed on the site.

## 🛠️ How it Works

1. **User Registration:** Users sign up as buyers or sellers.
2. **Listing Products:** Sellers add products via their dashboard.
3. **Browsing:** Buyers view the homepage which features dynamic sections managed by admins.
4. **Ordering:** Buyers add items to the cart and checkout. Orders are recorded in the database.
5. **Fulfillment:** Sellers/Admins view orders and process them.

For setup instructions, please refer to the [README.md](README.md).
