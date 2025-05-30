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

**Note: This High-level Task Breakdown represents the initial project planning structure organized by milestones. For current implementation sequencing and prioritization, please refer to the Consolidated Implementation Plan section below, which organizes these same tasks into execution phases.**

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

## Consolidated Implementation Plan

### Completed Work
- [x] **Milestone 1: Project Setup & Core Infrastructure** ✅ COMPLETE
- [x] **Milestone 2: Student Submission Workflow** ✅ COMPLETE
- [x] **Phase 1: Critical Bug Fixes** ✅ COMPLETE
   - Form field naming mismatch fixed
   - Database integration issues resolved
   - Redirect functionality working properly

### Phase 2: Core Workflow Implementation (Current Focus)

#### 1. Staff Dashboard Development
- [ ] **Apple-Style Dashboard Page**
  * Implement status-based tabs with badge counts
  * Create responsive layout grid adhering to 8pt spacing
  * Implement job listing components
  * Add database queries to retrieve jobs by status
  * **Success Criteria**: Staff can view all jobs with proper status filtering

#### 2. Job Status Management
- [ ] **Approval/Rejection Functionality**
  * Create modal interfaces for approve/reject actions
  * Implement database status updates with event logging
  * Add file movement between status directories (Uploaded → Pending)
  * **Success Criteria**: Staff can approve/reject jobs with proper state changes

#### 3. Student Confirmation Workflow
- [ ] **Token-Based Confirmation System**
  * Implement secure token generation and storage
  * Create confirmation email template
  * Build confirmation page UI and routing
  * Implement token validation logic
  * Add file movement (Pending → ReadyToPrint) upon confirmation
  * **Success Criteria**: Students can securely confirm jobs via email links

### Phase 3: Enhanced Management Features

#### 4. Metadata and File Operations
- [ ] **Metadata Management**
  * Implement metadata.json updates when job details change
  * Create slicer data input UI (weight, time)
  * Implement cost calculation based on weight/time
  * **Success Criteria**: Staff can update job details with proper persistence

#### 5. Direct File Integration
- [ ] **File Access Integration**
  * Implement SlicerOpener.py protocol handler
  * Create Windows registry integration for protocol
  * Add direct file opening buttons in dashboard
  * **Success Criteria**: Staff can open files directly in slicer software

#### 6. Status Transition System
- [ ] **Complete Workflow States**
  * Implement remaining status transitions:
    * ReadyToPrint → Printing
    * Printing → Completed
    * Completed → PaidPickedUp
  * Add UI for all workflow state changes
  * Ensure proper event logging throughout
  * **Success Criteria**: Full job lifecycle is manageable through the UI

### Phase 4: Communication and Asynchronous Features

#### 7. Notification System
- [ ] **Email Integration**
  * Set up Office 365 SMTP configuration
  * Create email templates for all notifications
  * Implement notification triggers throughout workflow
  * **Success Criteria**: All relevant status changes trigger appropriate emails

#### 8. Asynchronous Processing
- [ ] **Task Queue Implementation**
  * Set up Celery or RQ infrastructure
  * Configure task workers and monitoring
  * Migrate email sending to async tasks
  * **Success Criteria**: System handles background tasks reliably

#### 9. Thumbnail Generation
- [ ] **3D Preview System**
  * Implement STL/OBJ thumbnail generation
  * Add error handling for generation failures
  * Integrate thumbnails in dashboard UI
  * **Success Criteria**: Job listings display preview thumbnails when available

### Phase 5: Refinement and Production Readiness

#### 10. Testing and Documentation
- [ ] **Comprehensive Testing**
  * Write unit tests for core functionality
  * Implement integration tests for workflows
  * Add UI automation for critical paths
  * **Success Criteria**: Test suite validates all critical functionality

#### 11. UI/UX Verification
- [ ] **Accessibility and Design Compliance**
  * Verify all components meet Apple HIG standards
  * Test with various screen sizes and devices
  * Validate accessibility features
  * **Success Criteria**: UI fully complies with Apple design standards

#### 12. Deployment Preparation
- [ ] **Production Configuration**
  * Finalize database configuration
  * Set up proper logging and monitoring
  * Create staff documentation
  * **Success Criteria**: System is ready for production use

### Advanced Enhancements (Time Permitting)

#### 13. Analytics and Reporting
- [ ] **Usage Analytics**
  * Implement job statistics dashboard
  * Add time-based reporting
  * Create material usage tracking
  * **Success Criteria**: Staff can view print service utilization metrics

#### 14. Batch Operations
- [ ] **Multi-Job Management**
  * Add batch status update capabilities
  * Implement bulk email notifications
  * Create job filtering and search
  * **Success Criteria**: Staff can efficiently manage multiple jobs simultaneously

#### 15. Mobile Optimization
- [ ] **Mobile Experience**
  * Enhance responsive design for small screens
  * Optimize touch interactions
  * Add mobile-specific UI improvements
  * **Success Criteria**: System is fully usable on mobile devices

## Lessons

*   PowerShell `mkdir` might have limitations with multiple arguments or very long path arguments compared to `bash`. Create directories individually or in smaller batches if issues arise.
*   Always verify directory/file creation steps, e.g., using `list_dir`, especially if terminal output is unusual or truncated.
*   All frontend development must reference and comply with the Apple UI Design Research document and UI Reference Guide. These documents serve as the foundation for our UI/UX implementation. 