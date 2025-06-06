# 3D Print System V3 Development Scratchpad

## Background and Motivation

Rebuilding a Flask-based 3D print job management system for an academic/makerspace setting operating as an **extremely small lab with at most two employees working as a duo, often on the same computer using a single, shared password**. The system handles workflow from student submission to completion, with file tracking, staff approval, and the ability to open uploaded files directly in local applications.

**Core Objectives:**
1. **Student submission process**: Upload 3D model files (.stl, .obj, .3mf) with metadata
2. **Staff approval workflow**: Review, slice files, approve/reject jobs  
3. **Enhanced operational dashboard**: Real-time auto-updating interface with audio notifications and visual alerts
4. **File lifecycle management**: Track original files; manage authoritative files post-slicing; embed metadata.json
5. **Job status tracking & Event Logging**: Clear progression through status workflow with immutable event log
6. **Email notifications**: Asynchronously send automated updates to students
7. **Direct file opening**: Custom protocol handler to open local files in slicer software

**Target Environment**: System can run on up to two staff computers, as long as both use the same shared storage and database.

## Key Challenges and Analysis

### Technical Architecture Requirements
- **Backend**: Modular Flask (Blueprints) with SQLAlchemy (PostgreSQL)
- **Frontend**: Tailwind CSS with professional card-style UI, Alpine.js for interactivity  
- **Task Queue**: Celery or RQ for asynchronous processing (emails, thumbnails)
- **Authentication**: Simple staff-wide shared password with session management
- **File Storage**: Shared network storage with standardized naming and status-based directory structure
- **Email**: Flask-Mail with Office 365 SMTP integration
- **Database**: PostgreSQL with Flask-Migrate for schema management
- **Time Display**: Central Time (America/Chicago) with automatic DST handling
- **Pricing**: Weight-based ($0.10/gram filament, $0.20/gram resin, $3.00 minimum)

### Critical Dependencies
- Flask-WTF for form handling and CSRF protection
- WTForms with EmailValidator, DataRequired, Length validators
- email-validator>=2.0.0 (essential for form validation)
- pytz>=2023.3 (required for timezone handling)
- Celery/RQ dependencies for async processing
- ImageMagick (for thumbnail generation)

### Job Lifecycle (Event-Driven)
1. **Uploaded**: Student submits → file stored, metadata.json created, thumbnail task queued
2. **Pending**: Staff approves → confirmation email sent, awaiting student confirmation
3. **Rejected**: Staff rejects → rejection email sent with reasons
4. **ReadyToPrint**: Student confirms → file moved to print queue
5. **Printing**: Staff marks as printing → job in progress
6. **Completed**: Staff marks complete → completion email sent
7. **PaidPickedUp**: Student collects → final state

## High-Level Task Breakdown

### 🎯 CURRENT PRIORITY: Core System Implementation

#### Phase 1: Database Foundation (NEXT)
**Objective**: Establish robust PostgreSQL database with proper models and migrations

**Tasks**:
- [ ] **1.1: Core Models Implementation**
  - [ ] Create Job model with all required fields (id, student info, file paths, status, timestamps)
  - [ ] Create Event model for immutable audit logging
  - [ ] Define status enums and relationships
  - [ ] Success Criteria: Models created, relationships defined

- [ ] **1.2: Database Configuration**
  - [ ] Set up PostgreSQL connection configuration
  - [ ] Configure Flask-Migrate for schema management
  - [ ] Create initial migration files
  - [ ] Success Criteria: Database connects, migrations run successfully

- [ ] **1.3: Model Validation**
  - [ ] Test model creation and querying
  - [ ] Verify event logging functionality
  - [ ] Test status transitions
  - [ ] Success Criteria: All model operations work correctly

#### Phase 2: File Management System
**Objective**: Implement robust file handling with status-based directories and metadata

**Tasks**:
- [ ] **2.1: File Service Implementation**
  - [ ] Create file_service.py with status-based directory management
  - [ ] Implement standardized naming convention: FirstAndLastName_PrintMethod_Color_SimpleJobID.ext
  - [ ] Add metadata.json embedding for file resilience
  - [ ] Success Criteria: Files can be moved between status directories with metadata preserved

- [ ] **2.2: Directory Structure Setup**
  - [ ] Create storage directories: Uploaded/, Pending/, ReadyToPrint/, Printing/, Completed/, PaidPickedUp/
  - [ ] Implement file movement logic between directories
  - [ ] Add error handling for file operations
  - [ ] Success Criteria: Complete file lifecycle management working

#### Phase 3: Core Workflow Routes
**Objective**: Implement student submission and staff approval workflows

**Tasks**:
- [ ] **3.1: Student Submission Routes**
  - [ ] Implement submission form with comprehensive validation
  - [ ] Add file upload handling with security checks
  - [ ] Create success/confirmation pages
  - [ ] Success Criteria: Students can submit jobs successfully

- [ ] **3.2: Staff Dashboard Routes**
  - [ ] Implement login system with shared password
  - [ ] Create dashboard with status-based job filtering
  - [ ] Add job approval/rejection functionality
  - [ ] Success Criteria: Staff can manage job workflow

- [ ] **3.3: Status Transition Handling**
  - [ ] Implement job status updates with event logging
  - [ ] Add file movement during status changes
  - [ ] Create confirmation workflow for students
  - [ ] Success Criteria: Complete job lifecycle functional

#### Phase 4: Enhanced Dashboard Features
**Objective**: Add real-time updates, audio alerts, and visual indicators

**Tasks**:
- [ ] **4.1: Auto-Updating Dashboard**
  - [ ] Implement JavaScript polling with 45-second intervals
  - [ ] Create lightweight JSON API endpoints
  - [ ] Add "last updated" timestamp display
  - [ ] Success Criteria: Dashboard refreshes automatically

- [ ] **4.2: Audio Notification System**
  - [ ] Integrate Browser Audio API for new job alerts
  - [ ] Add user preference controls for sound
  - [ ] Store sound files in /static/sounds/
  - [ ] Success Criteria: Staff receive audio alerts for new uploads

- [ ] **4.3: Visual Alert System**
  - [ ] Implement "NEW" badge system for unreviewed jobs
  - [ ] Add persistent alert states until staff acknowledgment
  - [ ] Create "Mark as Reviewed" functionality
  - [ ] Success Criteria: Visual indicators guide staff attention

#### Phase 5: Asynchronous Processing
**Objective**: Implement background tasks for email and thumbnail generation

**Tasks**:
- [ ] **5.1: Task Queue Setup**
  - [ ] Choose and configure Celery or RQ
  - [ ] Set up worker processes
  - [ ] Create task definitions in processing.py
  - [ ] Success Criteria: Background tasks can be queued and executed

- [ ] **5.2: Email Service**
  - [ ] Implement email_service.py with Flask-Mail
  - [ ] Configure Office 365 SMTP settings
  - [ ] Create email templates for all job status changes
  - [ ] Success Criteria: Automated emails sent for job status updates

- [ ] **5.3: Thumbnail Generation**
  - [ ] Implement thumbnail_service.py with ImageMagick
  - [ ] Add graceful failure handling for unsupported files
  - [ ] Make thumbnail generation asynchronous
  - [ ] Success Criteria: Thumbnails generated without blocking workflow

#### Phase 6: Advanced Features
**Objective**: Complete system with protocol handler and production features

**Tasks**:
- [ ] **6.1: Direct File Opening**
  - [ ] Create SlicerOpener.py protocol handler
  - [ ] Implement OS-level integration for 3dprint:// protocol
  - [ ] Add security validation and logging
  - [ ] Success Criteria: Staff can open files directly in slicer software

- [ ] **6.2: Time and Cost Services**
  - [ ] Implement timezone handling with pytz (Central Time)
  - [ ] Create cost calculation service with weight-based pricing
  - [ ] Add time input rounding (always UP to nearest 0.5 hours)
  - [ ] Success Criteria: Accurate time display and cost calculations

## Project Status Board

### ✅ COMPLETED
- [x] **UI Foundation**: Professional interface design implemented (see [v0dev-implementation-board.md](v0dev-implementation-board.md))
- [x] **Template Architecture**: Modular component-based system established
- [x] **Form Validation**: Client and server-side validation working
- [x] **Basic Flask Structure**: Blueprints and routing framework ready

### 🔄 IN PROGRESS
**Current Focus**: Phase 1.1 - Core Models Implementation

### 📋 PENDING
- Database setup and configuration
- File management system implementation  
- Core workflow routes
- Enhanced dashboard features
- Asynchronous processing
- Advanced features

## Current Status / Progress Tracking

**Last Updated**: Ready to begin core system implementation

**Immediate Next Step**: Phase 1.1 - Create Job and Event models with PostgreSQL configuration

**Blockers**: None identified - ready to proceed with database implementation

**Dependencies Ready**:
- ✅ Flask application structure established
- ✅ Professional UI components available
- ✅ Form validation system working
- ⏳ PostgreSQL database setup needed
- ⏳ Task queue configuration needed

## Executor's Feedback or Assistance Requests

### Ready for Next Implementation Phase

**Phase 1.1 (Database Models) is ready to begin**:
- All UI components are in place and tested
- Flask application structure is established
- Ready to implement core Job and Event models
- PostgreSQL configuration needs to be set up

**Technical Questions for Implementation**:
1. Should we use local PostgreSQL installation or Docker container?
2. Preferred task queue: Celery (more features) or RQ (simpler setup)?
3. Email configuration: Use development SMTP or configure Office 365 immediately?

**No Blockers Identified**: Ready to proceed with Phase 1.1 implementation

## Lessons

### Technical Implementation Lessons
- **Read files before editing**: Always check current state before making modifications
- **Include debugging info**: Program output should contain useful troubleshooting information  
- **File validation**: Always validate file paths and operations before execution
- **Error handling**: Implement graceful degradation for all external dependencies
- **Database transactions**: Use atomic operations for multi-step database changes

### UI/UX Implementation Lessons  
- **Form validation**: Real-time client-side validation with server-side verification required
- **Error states**: Visual feedback with red borders and clear error messages
- **Loading states**: Show progress indicators for all async operations
- **Mobile responsiveness**: Test all components on various screen sizes
- **Accessibility**: Ensure keyboard navigation and screen reader compatibility

### Development Process Lessons
- **Component architecture**: Modular templates significantly improve maintainability
- **Version control**: Document all major changes and architectural decisions
- **Configuration management**: Use environment variables for all deployment-specific settings
- **Testing strategy**: Validate each component before integration
- **Dependencies**: Keep exact version requirements for critical packages (email-validator>=2.0.0, pytz>=2023.3) 