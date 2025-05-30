# 3D Print System Project Scratchpad

## Background and Motivation

This project will rebuild a Flask-based 3D print job management system, specifically tailored for an academic/makerspace setting operating as an **extremely small lab with at most two employees working as a duo, often on the same computer using a single, shared password**. The system will handle the workflow from student submission to completion, with file tracking, staff approval, and the ability to open the exact uploaded files directly in local applications.

The project aims to replace potentially ad-hoc or manual 3D print request systems with a **centralized, digitally managed, and workflow-driven platform.** It prioritizes clarity, efficiency, accurate file tracking, and a **strong, non-fragile foundation**, especially addressing the complexities of file changes introduced by slicer software and ensuring resilience. It leverages **modularity, explicit event-driven workflow management, asynchronous processing, and resilient data handling** to improve the experience for both students and the minimal staff managing the service.

## Key Challenges and Analysis

Based on the `masterplanV3.md`, key challenges and areas requiring careful attention include:

1.  **Robust File Management**: Ensuring the integrity and correct tracking of files through various stages (upload, slicing, storage) is critical. The use of `metadata.json` and a clear directory structure is a good approach. Standardized file naming will also be important.
2.  **Event-Driven Workflow**: Implementing an immutable event log for all job status changes and actions will be central to the system's reliability and auditability.
3.  **Asynchronous Task Handling**: Correctly setting up and managing asynchronous tasks (e.g., for email notifications, thumbnail generation) using Celery or RQ is crucial for performance and responsiveness.
4.  **Apple-Style User Experience (UX)**: All frontend development must strictly adhere to Apple's Human Interface Guidelines and design philosophy, following the principles documented in our UI reference guides:
    - Clarity: Prioritize legibility, white space, and intuitive layouts
    - Deference: Let content lead; avoid flashy UI elements
    - Depth: Use translucent panels and subtle shadows (max 3 layers)
    - Consistency: Maintain standardized patterns throughout
    - Simplicity: Strip to essential elements
    - Efficiency: Optimize interaction paths
    - Accessibility: Support Dynamic Type, high contrast, and reduced motion
5.  **Database Design and Interaction**: Proper setup of PostgreSQL, SQLAlchemy models (`Job`, `Event`), and migrations is fundamental.
6.  **Direct File Opening**: Implementing the custom protocol handler for opening files in local slicer software will require careful OS-level integration.
7.  **Modularity**: Adhering to the planned modular structure using Flask Blueprints will be important for maintainability.
8.  **Error Handling and Resilience**: The system needs to be robust against common issues, especially around file operations and external service integrations (e.g., email).
9.  **Security**: While authentication is simplified (shared password), ensuring protection against common web vulnerabilities (CSRF, XSS) is still necessary, likely via Flask-WTF.


## High-level Task Breakdown

This is an initial breakdown. Tasks will be refined and made more granular as the project progresses.

1.  **Project Setup & Core Infrastructure (Milestone 1)**
    *   [x] Initialize Flask application structure (as per `masterplanV3.md`).
        *   Success Criteria: Basic Flask app runs; directory structure created.
    *   [x] Configure PostgreSQL database and SQLAlchemy.
        *   Success Criteria: Database connection established; SQLAlchemy initialized.
    *   [x] Implement `Job` and `Event` SQLAlchemy models.
        *   Success Criteria: Models defined; initial migration created and applied.
    *   [x] Set up Flask-Migrate for database schema management.
        *   Success Criteria: Migrations can be generated and applied.
    *   [x] Implement basic staff authentication (shared password, session management).
        *   Success Criteria: Staff can log in to a protected area.
    *   [x] Create base HTML templates and static file setup following Apple UI/UX guidelines:
        *   Set up Tailwind CSS with custom configuration for Apple-style spacing (8pt grid)
        *   Configure system font stack (SF Pro / system-ui)
        *   Implement base component styles adhering to Apple's design principles
        *   Success Criteria: Base UI components match Apple's aesthetic; spacing follows 8pt grid; typography uses correct system fonts

2.  **Student Submission Workflow (Milestone 2)**
    *   [x] Create initial student submission form layout and visual hierarchy
        *   Success Criteria: Form layout matches design requirements with proper grouping and spacing
    *   [x] Implement dynamic field behavior
        *   Success Criteria: Color dropdown properly enables/disables and updates based on print method
    *   [x] Enhance form with Apple UI/UX compliance:
        *   Configure Tailwind for Apple design system (8pt grid, colors, typography)
        *   Update visual components to match Apple style
        *   Implement proper form control sizing and spacing
        *   Add appropriate depth and translucency effects
        *   Success Criteria: Form fully complies with Apple HIG specifications
    *   [x] Implement client-side validation and error feedback
        *   Success Criteria: Real-time validation with Apple-style error states and messaging
    *   [x] Implement file upload handling (validation, standardized naming, storage in `storage/Uploaded/`).
        *   Success Criteria: Files are uploaded, renamed, and stored correctly; invalid files are rejected.
    *   [x] Implement `metadata.json` creation alongside the uploaded file.
        *   Success Criteria: `metadata.json` is created with correct initial job data.
    *   [x] Implement `JobCreated` event logging.
        *   Success Criteria: An `Event` record is created in the database when a job is submitted.
    *   [x] Create the submission success page (`/submit/success`).
        *   Success Criteria: Success page displays job ID and next steps with Apple-style aesthetics.
    *   [ ] (Optional/Parallel) Setup asynchronous task queue (Celery/RQ).
        *   Success Criteria: Task queue is operational; test task can be executed.
    *   [ ] (Optional/Parallel) Implement asynchronous thumbnail generation.
        *   Success Criteria: Thumbnails are generated for uploaded files and stored; failures are handled gracefully.

3.  **Staff Dashboard & Job Management (Milestone 3)**
    *   [ ] Create basic staff dashboard page following Apple design principles:
        *   Implement proper layout grid and spacing
        *   Use Apple-style cards and list views
        *   Add appropriate visual hierarchy and typography
        *   Success Criteria: Dashboard matches Apple aesthetic while maintaining functionality
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
    *   [ ] Final UI/UX compliance verification:
        *   Verify all interactive elements meet 44x44pt minimum size
        *   Confirm proper contrast ratios (≥4.5:1)
        *   Test motion/animation behaviors
        *   Validate Dynamic Type and reduced motion support
        *   Success Criteria: UI fully complies with Apple HIG specifications
    *   [ ] Finalize configuration for production (if applicable, though lab setup is primary).
        *   Success Criteria: Configuration is secure and appropriate for the lab environment.
    *   [ ] Documentation for staff.
        *   Success Criteria: Basic usage guide for staff is created.

## Project Status Board

*   [x] **Milestone 1: Project Setup & Core Infrastructure** ⭐ COMPLETE
    *   [x] Initialize Flask application structure
    *   [x] Configure PostgreSQL database and SQLAlchemy
    *   [x] Implement `Job` and `Event` SQLAlchemy models
    *   [x] Set up Flask-Migrate
    *   [x] Implement basic staff authentication
    *   [x] Create base HTML templates and static file setup

*   [x] **Milestone 2: Student Submission Workflow** ⭐ PARTIALLY COMPLETE
    *   [x] Redesign the Form Layout and Visual Hierarchy for /submit (static HTML/CSS only)
    *   [x] Implement Dynamic Field Behavior
    *   [x] Implement Backend Submission Handler (POST route for /submit)
    *   [x] Implement file upload handling (validation, standardized naming, storage)
    *   [x] Implement `metadata.json` creation alongside uploaded file
    *   [ ] Implement `JobCreated` event logging in database ❌ BUG FOUND
    *   [ ] Create submission success page routing logic ❌ BUG FOUND

*   [ ] **Milestone 3: Staff Dashboard & Job Management** ⭐ NEXT PRIORITY
    *   [ ] Create Apple-style dashboard page
    *   [ ] Implement job status update functionality
    *   [ ] Implement file movement based on status changes
    *   [ ] Implement `metadata.json` updates
    *   [ ] Implement slicer data input functionality
    *   [ ] Implement cost calculation
    *   [ ] Implement direct file opening

*   [ ] **Milestone 4: Notifications & Final Workflow Steps**
    *   [ ] Implement email notifications
    *   [ ] Implement remaining job status transitions

*   [ ] **Milestone 5: Refinements, Testing & Deployment Prep**
    *   [ ] Comprehensive testing
    *   [ ] Final UI/UX compliance verification
    *   [ ] Finalize configuration
    *   [ ] Documentation for staff

*   [x] **Apple UI/UX Compliance Updates** ⭐ COMPLETE
    *   [x] Configure Tailwind for Apple-style design system
    *   [x] Update existing components to Apple guidelines
    *   [x] Enhance accessibility features
    *   [x] Review and update animations/transitions
    *   [x] Test across different screen sizes and orientations

*   [x] **Project Cleanup & Optimization** ⭐ COMPLETE
    *   [x] Phase 1: Dead Code Elimination (17.5KB+ removed)
    *   [x] Phase 2: Route Structure & Backend Implementation  
    *   [x] Phase 3: Configuration Standardization (secure .env setup)
    *   [x] Phase 4: Static File Optimization (24.7KB optimal footprint)

## Current System Status & Development Plan

### Issues Identified

1. **Database Integration**: Files are uploaded but no job records are created in the database
2. **Redirect Failure**: No redirect to success page after form submission
3. **Form Field Mismatch**: Form submission returns field error "Missing: Studentname" despite the field being filled
4. **Staff Dashboard**: Implementation incomplete
5. **Job Status Workflow**: Not implemented
6. **Email Authentication**: Fails with test credentials

### Root Cause Analysis

Many of these issues appear to be related to incomplete implementation rather than bugs in existing code. The system has the basic structure in place but is missing critical connective functionality:

1. **Form Field Naming Inconsistency**: The backend is likely expecting camelCase fields (studentName) while the frontend sends snake_case fields (student_name)
2. **Database Integration Gap**: The file service is working, but the database transaction is likely failing silently
3. **Missing Redirect Logic**: The success redirection is not being triggered after successful submission

### Development Plan

We'll adopt a hybrid approach that balances bug fixes with continued implementation:

#### Phase 1: Critical Path Bug Fixes First

1. **Fix Form Field Naming Mismatch** (1-2 hours)
   - This is causing the "Missing: Studentname" error
   - Likely a simple mismatch between form field names and what the backend expects
   - Quick win that enables successful form submission

2. **Fix Database Integration** (4-6 hours)
   - Files upload but no database records are created
   - Need to debug transaction handling and ensure proper error logging
   - Critical for tracking job status and progression

3. **Fix Redirect Logic** (1 hour)
   - Ensure successful submissions redirect to the success page
   - Completes the basic submission flow

#### Phase 2: Implement Core Workflow (Parallel Development)

Once the critical bugs are fixed, we should implement the core workflow components in priority order:

1. **Staff Dashboard - Basic Job List** (6-8 hours)
   - Implement the dashboard with status-based tabs
   - Add job listing functionality with filters
   - This allows staff to see submitted jobs

2. **Job Status Management** (8-10 hours)
   - Implement approval/rejection functionality
   - Add file movement between status directories
   - Add status change events and logging

3. **Student Confirmation Flow** (6-8 hours)
   - Implement token generation
   - Create confirmation page and handling
   - Enable file movement to ReadyToPrint status

#### Phase 3: Complete the System (Final Features)

1. **Email Integration** (4-6 hours)
   - Set up proper email templates
   - Implement asynchronous sending
   - Add notification points in workflow

2. **Protocol Handler** (if needed) (8-10 hours)
   - Implement SlicerOpener.py
   - Configure registry integration

## Lessons

*   PowerShell `mkdir` might have limitations with multiple arguments or very long path arguments compared to `bash`. Create directories individually or in smaller batches if issues arise.
*   Always verify directory/file creation steps, e.g., using `list_dir`, especially if terminal output is unusual or truncated.
*   All frontend development must reference and comply with the Apple UI Design Research document and UI Reference Guide. These documents serve as the foundation for our UI/UX implementation. 