# Migrating a Monolithic E-Commerce Application to a Microservices Architecture

## Description

The project's primary objective is to transition an e-commerce web application into a microservices architecture. This web application has the following features:
1. **User Login/Registration**
2. **Product Browsing Page**: Display all available products together.
3. **Product Landing Page**: Description/Price for that particular product.
4. **Cart**: After adding products.
5. **Checkout/Payment Page**


## Tech Stack

- **Backend**: Flask with MongoDB/Mongo Express
- **Frontend**: React with MongoDB


## Migration Strategy

Each discrete functionality of the application will be converted into a standalone microservice.

To facilitate the migration process, we have explored the **Strangler Pattern**. This pattern involves gradually replacing parts of the existing monolithic application with microservices, ensuring minimal disruption to the overall system while modernizing its architecture.

## Features

- **User Login/Registration**
- **Product Browsing Page**: Display all available products together.
- **Product Landing Page**: Description/Price for that particular product.
- **Cart**: After adding products.
- **Checkout/Payment Page**

