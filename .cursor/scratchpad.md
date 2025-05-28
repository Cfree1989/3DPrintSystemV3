# 3D Print System Project Scratchpad

## Background and Motivation

This project will rebuild a Flask-based 3D print job management system, specifically tailored for an academic/makerspace setting operating as an **extremely small lab with at most two employees working as a duo, often on the same computer using a single, shared password**. The system will handle the workflow from student submission to completion, with file tracking, staff approval, and the ability to open the exact uploaded files directly in local applications.

The project aims to replace potentially ad-hoc or manual 3D print request systems with a **centralized, digitally managed, and workflow-driven platform.** It prioritizes clarity, efficiency, accurate file tracking, and a **strong, non-fragile foundation**, especially addressing the complexities of file changes introduced by slicer software and ensuring resilience. It leverages **modularity, explicit event-driven workflow management, asynchronous processing, and resilient data handling** to improve the experience for both students and the minimal staff managing the service.

## Key Challenges and Analysis

Based on the `masterplanV3.md`, key challenges and areas requiring careful attention include:

1.  **Robust File Management**: Ensuring the integrity and correct tracking of files through various stages (upload, slicing, storage) is critical. The use of `metadata.json` and a clear directory structure is a good approach. Standardized file naming will also be important.
2.  **Event-Driven Workflow**: Implementing an immutable event log for all job status changes and actions will be central to the system's reliability and auditability.
3.  **Asynchronous Task Handling**: Correctly setting up and managing asynchronous tasks (e.g., for email notifications, thumbnail generation) using Celery or RQ is crucial for performance and responsiveness.
4.  **User Experience (UX)**: The submission form has specific dynamic behaviors and detailed informational text requirements that must be implemented accurately.
5.  **Database Design and Interaction**: Proper setup of PostgreSQL, SQLAlchemy models (`Job`, `Event`), and migrations is fundamental.
6.  **Direct File Opening**: Implementing the custom protocol handler for opening files in local slicer software will require careful OS-level integration.
7.  **Modularity**: Adhering to the planned modular structure using Flask Blueprints will be important for maintainability.
8.  **Error Handling and Resilience**: The system needs to be robust against common issues, especially around file operations and external service integrations (e.g., email).
9.  **Security**: While authentication is simplified (shared password), ensuring protection against common web vulnerabilities (CSRF, XSS) is still necessary, likely via Flask-WTF.

## High-level Task Breakdown

This is an initial breakdown. Tasks will be refined and made more granular as the project progresses.

1.  **Project Setup & Core Infrastructure (Milestone 1)**
    *   [ ] Initialize Flask application structure (as per `masterplanV3.md`).
        *   Success Criteria: Basic Flask app runs; directory structure created.
    *   [ ] Configure PostgreSQL database and SQLAlchemy.
        *   Success Criteria: Database connection established; SQLAlchemy initialized.
    *   [ ] Implement `Job` and `Event` SQLAlchemy models.
        *   Success Criteria: Models defined; initial migration created and applied.
    *   [ ] Set up Flask-Migrate for database schema management.
        *   Success Criteria: Migrations can be generated and applied.
    *   [ ] Implement basic staff authentication (shared password, session management).
        *   Success Criteria: Staff can log in to a protected area.
    *   [ ] Create base HTML templates and static file setup (Tailwind CSS, Alpine.js if chosen).
        *   Success Criteria: Basic site structure visible; CSS and JS loaded.

2.  **Student Submission Workflow (Milestone 2)**
    *   [ ] Create the student submission form (`/submit`) with all specified fields, validations (client-side and server-side), and introductory text.
        *   Success Criteria: Form renders correctly; all fields present; client-side validation works as described; introductory text is exactly as specified.
    *   [ ] Implement file upload handling (validation, standardized naming, storage in `storage/Uploaded/`).
        *   Success Criteria: Files are uploaded, renamed, and stored correctly; invalid files are rejected.
    *   [ ] Implement `metadata.json` creation alongside the uploaded file.
        *   Success Criteria: `metadata.json` is created with correct initial job data.
    *   [ ] Implement `JobCreated` event logging.
        *   Success Criteria: An `Event` record is created in the database when a job is submitted.
    *   [ ] Create the submission success page (`/submit/success`).
        *   Success Criteria: Success page displays job ID and next steps.
    *   [ ] (Optional/Parallel) Setup asynchronous task queue (Celery/RQ).
        *   Success Criteria: Task queue is operational; test task can be executed.
    *   [ ] (Optional/Parallel) Implement asynchronous thumbnail generation.
        *   Success Criteria: Thumbnails are generated for uploaded files and stored; failures are handled gracefully.

3.  **Staff Dashboard & Job Management (Milestone 3)**
    *   [ ] Create basic staff dashboard page.
        *   Success Criteria: Staff can view a list of submitted jobs.
    *   [ ] Implement job status update functionality (e.g., Approve, Reject).
        *   Success Criteria: Staff can change job statuses; corresponding events are logged.
    *   [ ] Implement file movement based on status changes (e.g., to `storage/Pending/`).
        *   Success Criteria: Files are moved to correct directories as status changes.
    *   [ ] Implement `metadata.json` updates when job details change (e.g., after slicing by staff).
        *   Success Criteria: `metadata.json` is updated with new information.
    *   [ ] Implement functionality for staff to input slicer-generated data (weight, time).
        *   Success Criteria: Staff can add/update weight and time for a job.
    *   [ ] Implement cost calculation based on weight and time.
        *   Success Criteria: Costs are calculated correctly according to the pricing model.
    *   [ ] Implement direct file opening (custom protocol handler integration - may require separate script `SlicerOpener.py`).
        *   Success Criteria: Staff can click a link/button to open the job file in the default local slicer application.

4.  **Notifications & Final Workflow Steps (Milestone 4)**
    *   [ ] Implement email notifications for job status changes (Approved, Rejected, Completed) using asynchronous tasks.
        *   Success Criteria: Students receive email notifications for relevant status changes.
    *   [ ] Implement remaining job status transitions and associated logic (ReadyToPrint, Printing, Completed, PaidPickedUp).
        *   Success Criteria: Full job lifecycle can be managed through the system; events logged for each transition.

5.  **Refinements, Testing & Deployment Prep (Milestone 5)**
    *   [ ] Comprehensive testing (unit, integration, and UX tests based on requirements).
        *   Success Criteria: Test suite passes; manual testing confirms all features work as expected.
    *   [ ] Implement all required UI/UX details (dynamic form behavior, error handling, accessibility).
        *   Success Criteria: UI matches `masterplanV3.md` specifications.
    *   [ ] Finalize configuration for production (if applicable, though lab setup is primary).
        *   Success Criteria: Configuration is secure and appropriate for the lab environment.
    *   [ ] Documentation for staff.
        *   Success Criteria: Basic usage guide for staff is created.

## Project Status Board

*(To be filled by Executor as tasks are undertaken)*

*   [x] **Milestone 1: Project Setup & Core Infrastructure**
    *   [x] Initialize Flask application structure
    *   [ ] Configure PostgreSQL database and SQLAlchemy
    *   [ ] Implement `Job` and `Event` SQLAlchemy models
    *   [ ] Set up Flask-Migrate
    *   [ ] Implement basic staff authentication
    *   [ ] Create base HTML templates and static file setup
*   [ ] **Milestone 2: Student Submission Workflow**
    *   [ ] Create student submission form
    *   [ ] Implement file upload handling
    *   [ ] Implement `metadata.json` creation
    *   [ ] Implement `JobCreated` event logging
    *   [ ] Create submission success page
    *   [ ] (Optional) Setup asynchronous task queue
    *   [ ] (Optional) Implement asynchronous thumbnail generation
*   [ ] **Milestone 3: Staff Dashboard & Job Management**
    *   [ ] Create basic staff dashboard page
    *   [ ] Implement job status update functionality
    *   [ ] Implement file movement based on status changes
    *   [ ] Implement `metadata.json` updates
    *   [ ] Implement functionality for staff to input slicer-generated data
    *   [ ] Implement cost calculation
    *   [ ] Implement direct file opening
*   [ ] **Milestone 4: Notifications & Final Workflow Steps**
    *   [ ] Implement email notifications
    *   [ ] Implement remaining job status transitions
*   [ ] **Milestone 5: Refinements, Testing & Deployment Prep**
    *   [ ] Comprehensive testing
    *   [ ] Implement all required UI/UX details
    *   [ ] Finalize configuration
    *   [ ] Documentation for staff

## Executor's Feedback or Assistance Requests

*   Initial Flask app structure created. Basic Flask app `app.py` confirmed to start (ran in background).
*   Encountered some issues with `mkdir` in PowerShell when trying to create multiple directories at once or with very long paths; switched to creating them one by one, which worked. The `list_dir` command was crucial for verifying directory creation steps.
*   Initialized local Git repository, created `.gitignore`, and made initial commit. Pushed to GitHub remote: `https://github.com/Cfree1989/3DPrintSystemV3`.
*   Installed `Flask-SQLAlchemy`, `psycopg2-binary`, `python-dotenv`. Generated `requirements.txt`.
*   Updated `config.py`, `extensions.py`, and `app/__init__.py` to load database configuration and initialize SQLAlchemy.
*   Awaiting user to create `.env` file with `SECRET_KEY` and `DATABASE_URL`, and then test the application run to verify database URI loading.

## Lessons

*   PowerShell `mkdir` might have limitations with multiple arguments or very long path arguments compared to `bash`. Create directories individually or in smaller batches if issues arise.
*   Always verify directory/file creation steps, e.g., using `list_dir`, especially if terminal output is unusual or truncated. 