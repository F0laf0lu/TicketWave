# Ticketwave

Ticketwave is a Django-based ticketing API designed to simplify the management of events and ticket purchases. This project serves as a Minimum Viable Product (MVP) aimed at providing a foundational structure for a ticketing system.

## Description

Organizing and attending events can be complex, and Ticketwave aims to streamline the process by offering a straightforward API for event organizers and attendees. Whether you're hosting a conference, concert, or sports event, Ticketwave facilitates the creation, management, and purchase of event tickets.

### Key Features

- **Event Management:** Create, retrieve, update, and delete events with detailed information such as name, date, and venue.
- **Ticket Management:** Generate and manage tickets associated with specific events, including options for retrieval, update, and deletion.
- **Ticket Purchase:** Allow users to purchase tickets for their chosen events, creating a seamless experience for both event organizers and attendees.

### Why Ticketwave?

- **Simplicity:** Ticketwave is designed with simplicity in mind, providing essential features for event organizers and attendees without unnecessary complexity.
- **Customization:** While being a basic MVP, Ticketwave is easily extensible, allowing developers to customize and build upon its foundation.

## Getting Started

### Prerequisites

Ensure you have the following prerequisites installed:

- Python (version 3.x)
- Django (version 3.x)
- (Add any other dependencies)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/F0laf0lu/TicketWave.git
   ```

2. Navigate to the project directory:

    ```
        cd ticketwave
    ```

3. Install dependencies:

    ```
        pip install -r requirements.txt
    ```

4. Run migrations:

    ```
        python manage.py migrate
    ```


5. Start the development server::
    ```
        python manage.py runserver
    ```

6. The app is running at http://127.0.0.1:8000/. Open on your preferred broser



# API Endpoints

Ticketwave provides the following API endpoints to manage events and tickets:

- **List and Create Events:**
  - `/events/`: Endpoint to list all events and create new events.

- **Retrieve, Update, or Delete a Specific Event:**
  - `/events/<int:event_id>/`: Endpoint to retrieve, update, or delete a specific event.

- **List and Create Tickets for a Specific Event:**
  - `/events/<int:event_id>/tickets/`: Endpoint to list existing tickets for an event and create new tickets.

- **Create a Ticket for a Specific Event:**
  - `/events/<int:event_id>/get_ticket/`: Endpoint to create a new ticket for a specific event.

- **List and Create Tickets:**
  - `/ticket/`: Endpoint to list all tickets and create new tickets.

- **Retrieve, Update, or Delete a Specific Ticket:**
  - `/ticket/<int:ticket_id>/`: Endpoint to retrieve, update, or delete a specific ticket.

- **Access Swagger Documentation:**
  - `/swagger-docs/`: Endpoint to access Swagger documentation for the APIs.

# Contributing

We welcome contributions to enhance Ticketwave! If you'd like to contribute, please follow our [Contribution Guidelines](CONTRIBUTING.md). Your input is valuable, and we appreciate your efforts in making Ticketwave even better.

# License

This project is licensed under the [MIT License](LICENSE). Feel free to explore, use, and contribute to Ticketwave in accordance with the terms of the license.

