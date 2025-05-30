# Sound Notification Files

This directory contains audio files for the 3D Print System dashboard notifications.

## Required Sound Files

### Primary Notifications
- **`new-job.mp3`** - Main notification sound for new job uploads
  - Duration: 1-2 seconds
  - Volume: Moderate, office-appropriate
  - Tone: Pleasant, attention-getting but not jarring
  - Format: MP3, 44.1kHz, high quality

### Secondary Notifications (Future)
- **`job-approved.mp3`** - Job approval confirmation
- **`job-completed.mp3`** - Job completion alert
- **`error.mp3`** - System error notification

## Audio Specifications
- **Format**: MP3 (universal browser support)
- **Sample Rate**: 44.1kHz
- **Bit Rate**: 128kbps or higher
- **Duration**: 1-3 seconds maximum
- **Volume**: Normalized to appropriate office levels

## Usage
These files are loaded by the dashboard's audio notification system and played when:
- New jobs are detected during auto-refresh polling
- Important status changes occur
- System events require user attention

## Browser Compatibility
The system handles:
- Modern autoplay restrictions
- User interaction requirements
- Fallback for unsupported formats
- Graceful degradation when audio fails

## Implementation
Audio files are managed by the `SoundNotificationManager` class in the dashboard JavaScript. 