---
article: 
    publishedTime: "2025-06-19T02:07:41-08:00"
    modifiedTime: "2025-06-19T02:07:41-08:00"
    authors: ["Violet Monserate"]
    section: Class Projects
    tags: ["java", "postgres"]
layout: '@components/MarkdownProjectLayout.astro'
title: Flight App
description: Project for CSE 344 databases, bridging backend and frontend interaction with live, relational database
seoDescription: Project for CSE 344 databases, bridging backend and frontend interaction with live, relational database using Java and PostGres SQL database. 
image:
    src: "@assets/flightApp.png"
    alt: ER diagram for the Flight App, depicting the relationships between different ables and the entities contained within.
startDate: '2025-05'
finishDate: '2025-05'
icons: ["java", "postgres"]
---

![ER diagram for the Flight App, depicting the relationships between different ables and the entities contained within.](@assets/flightApp.png)

---

## Overview

In this project, I learned about how to link an application to a database, specifically through the use of JDBC, while also going through the whole process of designing a database, including generating an ER diagram to include every entity and relationship we'd possibly need. FlightApp functions as a complete client-server relational database application designed to manage airline flight reservations, ensuring data integrity and handling concurrent user operations in a shared environment.

## Tech Stack

- **Language:** Java
- **Database:** PostgreSQL
- **Connectivity:** Java Database Connectivity (JDBC)
- **Build Tool:** Maven
- **Concepts:** Relational Schema Design, Cryptography (Salting/Hashing), ACID Transactions, Deadlock Resolution

## Database Design

The foundation of the app required translating high-level business requirements into a conceptual Entity-Relationship (ER) model before mapping it to a physical schema. The database tracks several interconnected entities:

- **Users:** Stores account credentials and wallet balances.
- **Flights:** The base table detailing origin, destination, carrier, and capacity. 
- **Itineraries:** Tracks both direct and single-layover indirect flight combinations.
- **Reservations:** Connects users to itineraries and tracks payment statuses.

Primary and foreign key constraints were rigorously applied to maintain referential integrity across all custom tables.

## Concurrency and ACID Transactions

Because this is a multi-user client-server application, it was designed to handle multiple instances running in parallel without data corruption or race conditions. This meant stepping away from JDBC's default auto-commit behavior and manually defining transaction boundaries.

- **Isolation & Consistency:** Database operations for booking and paying are wrapped in explicit SQL transactions (`conn.setAutoCommit(false)`), ensuring that actions like deducting an account balance and confirming a reservation occur atomically.
- **Deadlock Handling:** When multiple clients compete for the same resources, the database engine occasionally throws transient deadlock exceptions (SQLStates `40001` or `40P01`). The application code automatically catches these specific SQL exceptions, rolls back safely, and retries the transaction.

## Security

To prevent SQL injection vulnerabilities, all database interactions that incorporate user input utilize JDBC `PreparedStatement` objects rather than dynamically concatenated strings. 

User authentication is secured using the PBKDF2 algorithm (`PBKDF2WithHmacSHA1`). Passwords are not stored in plaintext; instead, a cryptographically secure random salt is generated for each user, combined with the plaintext password, and hashed over 65,536 iterations. The resulting salted hash and the salt itself are concatenated and stored as a `BYTEA` type in the database.

## Debugging & Edge Cases

Ensuring the reservation logic correctly identified fully booked flights required navigating specific edge cases. Initially, the query checked if the number of existing reservations was strictly below the flight's total seat capacity. However, manual testing revealed flights in the system that had a recorded capacity of *zero*. 

To fix this, the capacity check was expanded to ensure that the flight itself has a seat count strictly greater than zero before any bookings can proceed, successfully avoiding phantom reservations on invalid or non-passenger aircraft.

![A command line UI asking user to 'create', 'login', 'search', 'book', 'pay', 'reservations', or 'quit'](@assets/flightApp.png) 
*Fig. 1: The command line UI asking user to 'create', 'login', 'search', 'book', 'pay', 'reservations', or 'quit'*

## Reflection 

### Technical Growth and JDBC
Navigating the constraints of this project—such as working without Java text blocks and managing a massive single-file codebase—was initially frustrating. However, working within these limitations forced a deeper, more disciplined understanding of the architecture. With practice from the earlier milestones, the debugging process became significantly more straightforward, and interacting with the backend server via JDBC became highly intuitive. Seeing the parallel transaction tests finally pass after writing all the necessary SQL and Java code was incredibly satisfying.

### Debugging
One of the most valuable takeaways was refining my debugging methodology, specifically when tracking down the bug where the system failed to recognize fully booked flights. The breakthrough didn't come from staring endlessly at the Java code, but from directly querying the server with different parameters and realizing a crucial edge case existed in the data itself: flights with an initial capacity of *zero*. 

If I were to give advice to a future developer tackling a similar database project, my process boils down to a couple things. For one, I always trust the spec and re-read the documentation and manually compare the outputs of your queries against the expected results provided in the assignment. Being around others working on the project was also helpful, as I'd be able to bounce ideas off of them("rubber ducky debugging") to walk through query logic step-by-step, explaining it as if those people were fetching the exact data you need. In addition, I learned how I shouldn't assume a bug's root cause is strictly tied to the title of the failing test. Keep an open mind and isolate variables when tracking down the issue.

### Evaluating Resources
This project highlighted the difference between resources that solve immediate problems versus those that build long-term foundational knowledge. In the heat of the moment, specific section slides on JDBC and transactions were lifesavers for resolving immediate compilation errors and syntax issues. 

However, looking at the bigger picture, the foundational practice from previous, more general homework assignments proved to be the most universally useful resource for understanding core database concepts like Primary Key and Foreign Key joins. Moving forward, the spec itself might not be needed, but this completed assignment codebase will undoubtedly serve as my own personal reference guide for how to build applications that interact with servers using JDBC.