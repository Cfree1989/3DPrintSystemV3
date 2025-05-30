# Sound Notification Files

This directory contains audio files for the 3D Print System dashboard notifications.

## Current Status
⚠️ **No audio files currently present** - System uses Web Audio API fallback beep sound

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

## Fallback System
When MP3 files are not available, the system automatically uses a Web Audio API generated beep:
- **Tone**: 800 Hz sine wave
- **Duration**: 0.5 seconds with fade out
- **Volume**: Moderate (30% gain)
- **Browser Support**: All modern browsers

## Audio Specifications
- **Format**: MP3 (universal browser support)
- **Sample Rate**: 44.1kHz
- **Bit Rate**: 128kbps or higher
- **Duration**: 1-3 seconds maximum
- **Volume**: Normalized to appropriate office levels

## Adding Real Audio Files
1. Create or obtain appropriate MP3 audio files
2. Place them in this directory (`3DPrintSystem/app/static/sounds/`)
3. Ensure filenames match exactly: `new-job.mp3`, `job-approved.mp3`, etc.
4. Test by toggling sound notifications in the dashboard

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
- Web Audio API fallback when files missing

## Implementation
Audio files are managed by the `SoundNotificationManager` class in the dashboard JavaScript with automatic fallback to Web Audio API when files are unavailable. 