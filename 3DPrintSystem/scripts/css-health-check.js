/**
 * CSS HEALTH CHECK SCRIPT
 * 3D Print System - Performance Monitoring
 * 
 * Monitors CSS loading, layout shifts, and overall UI performance
 * Detects issues with the new CSS architecture
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

// Configuration
const FLASK_URL = 'http://localhost:5000';
const HEALTH_CHECK_ENDPOINTS = [
  '/dashboard',
  '/submit',
  '/login'
];

const PERFORMANCE_THRESHOLDS = {
  cssLoadTime: 1000,      // 1 second max
  layoutShiftScore: 0.1,  // CLS threshold
  totalPageSize: 2000000, // 2MB max
  cssFileSize: 500000     // 500KB max for CSS
};

/**
 * Check CSS file accessibility and size
 */
async function checkCSSFiles(page) {
  console.log('\n🎨 Checking CSS file health...');
  
  const cssFiles = [
    '/static/css/main.css',
    '/static/css/base/variables.css',
    '/static/css/base/reset.css',
    '/static/css/components/tabs.css',
    '/static/css/components/buttons.css',
    '/static/css/components/cards.css',
    '/static/css/components/modals.css',
    '/static/css/components/forms.css',
    '/static/css/layouts/grid.css',
    '/static/css/layouts/containers.css'
  ];

  const results = [];

  for (const cssFile of cssFiles) {
    try {
      const response = await page.goto(`${FLASK_URL}${cssFile}`, { 
        waitUntil: 'networkidle2' 
      });
      
      const status = response.status();
      const size = await response.buffer().then(buffer => buffer.length);
      
      const result = {
        file: cssFile,
        status: status,
        size: size,
        sizeKB: Math.round(size / 1024),
        accessible: status === 200,
        withinSizeLimit: size < PERFORMANCE_THRESHOLDS.cssFileSize
      };

      if (result.accessible) {
        console.log(`   ✅ ${cssFile} (${result.sizeKB}KB)`);
      } else {
        console.log(`   ❌ ${cssFile} (HTTP ${status})`);
      }

      results.push(result);

    } catch (error) {
      console.log(`   ❌ ${cssFile} (Error: ${error.message})`);
      results.push({
        file: cssFile,
        status: 'ERROR',
        error: error.message,
        accessible: false
      });
    }
  }

  return results;
}

/**
 * Monitor layout shifts and CSS-related performance
 */
async function monitorLayoutShifts(page, url) {
  console.log(`\n📐 Monitoring layout shifts for ${url}...`);

  // Set up performance monitoring
  await page.evaluateOnNewDocument(() => {
    window.performanceData = {
      layoutShifts: [],
      cssLoadTimes: [],
      cssErrors: []
    };

    // Track layout shifts
    const observer = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (entry.entryType === 'layout-shift' && !entry.hadRecentInput) {
          window.performanceData.layoutShifts.push({
            value: entry.value,
            sources: entry.sources?.map(source => ({
              node: source.node?.tagName || 'unknown',
              currentRect: source.currentRect,
              previousRect: source.previousRect
            })) || []
          });
        }
      }
    });

    observer.observe({ entryTypes: ['layout-shift'] });

    // Track CSS load times
    const resourceObserver = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (entry.initiatorType === 'link' && entry.name.includes('.css')) {
          window.performanceData.cssLoadTimes.push({
            url: entry.name,
            loadTime: entry.responseEnd - entry.requestStart,
            size: entry.transferSize || 0
          });
        }
      }
    });

    resourceObserver.observe({ entryTypes: ['resource'] });

    // Track CSS errors
    window.addEventListener('error', (event) => {
      if (event.target.tagName === 'LINK' && event.target.rel === 'stylesheet') {
        window.performanceData.cssErrors.push({
          url: event.target.href,
          error: 'Failed to load CSS file'
        });
      }
    });
  });

  try {
    // Navigate and wait for page to load
    await page.goto(`${FLASK_URL}${url}`, { 
      waitUntil: 'networkidle2',
      timeout: 10000 
    });

    // Wait for any additional layout shifts to settle
    await page.waitForTimeout(2000);

    // Get performance data
    const performanceData = await page.evaluate(() => window.performanceData);

    // Calculate CLS (Cumulative Layout Shift)
    const clsScore = performanceData.layoutShifts
      .reduce((sum, shift) => sum + shift.value, 0);

    const avgCssLoadTime = performanceData.cssLoadTimes.length > 0
      ? performanceData.cssLoadTimes.reduce((sum, css) => sum + css.loadTime, 0) / performanceData.cssLoadTimes.length
      : 0;

    const result = {
      url: url,
      clsScore: clsScore,
      layoutShifts: performanceData.layoutShifts.length,
      cssLoadTimes: performanceData.cssLoadTimes,
      avgCssLoadTime: Math.round(avgCssLoadTime),
      cssErrors: performanceData.cssErrors,
      clsHealthy: clsScore < PERFORMANCE_THRESHOLDS.layoutShiftScore,
      cssLoadHealthy: avgCssLoadTime < PERFORMANCE_THRESHOLDS.cssLoadTime
    };

    // Log results
    if (result.clsHealthy) {
      console.log(`   ✅ Layout Stability: CLS = ${clsScore.toFixed(4)} (Good)`);
    } else {
      console.log(`   ⚠️  Layout Stability: CLS = ${clsScore.toFixed(4)} (Needs Improvement)`);
    }

    if (result.cssLoadHealthy) {
      console.log(`   ✅ CSS Load Time: ${result.avgCssLoadTime}ms (Good)`);
    } else {
      console.log(`   ⚠️  CSS Load Time: ${result.avgCssLoadTime}ms (Slow)`);
    }

    if (result.cssErrors.length === 0) {
      console.log(`   ✅ No CSS loading errors`);
    } else {
      console.log(`   ❌ CSS Errors: ${result.cssErrors.length}`);
      result.cssErrors.forEach(error => {
        console.log(`      - ${error.url}: ${error.error}`);
      });
    }

    return result;

  } catch (error) {
    console.log(`   ❌ Performance monitoring failed: ${error.message}`);
    return {
      url: url,
      error: error.message,
      clsHealthy: false,
      cssLoadHealthy: false
    };
  }
}

/**
 * Check accessibility basics
 */
async function checkAccessibility(page, url) {
  console.log(`\n♿ Checking accessibility for ${url}...`);

  try {
    await page.goto(`${FLASK_URL}${url}`, { waitUntil: 'networkidle2' });

    // Check basic accessibility features
    const accessibilityChecks = await page.evaluate(() => {
      const results = {};

      // Check for skip links
      const skipLinks = document.querySelectorAll('a[href="#main-content"], .sr-only');
      results.hasSkipLinks = skipLinks.length > 0;

      // Check form labels
      const inputs = document.querySelectorAll('input, select, textarea');
      const inputsWithLabels = Array.from(inputs).filter(input => {
        const label = document.querySelector(`label[for="${input.id}"]`) || 
                     input.closest('label') ||
                     input.getAttribute('aria-label') ||
                     input.getAttribute('aria-labelledby');
        return label;
      });
      results.formLabelsRatio = inputs.length > 0 ? inputsWithLabels.length / inputs.length : 1;

      // Check heading hierarchy
      const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
      results.hasHeadings = headings.length > 0;

      // Check color contrast (basic check)
      const buttons = document.querySelectorAll('button, .btn, .btn-v0-primary, .btn-v0-secondary');
      results.buttonCount = buttons.length;

      // Check ARIA attributes
      const elementsWithAria = document.querySelectorAll('[role], [aria-label], [aria-labelledby], [aria-describedby]');
      results.ariaElements = elementsWithAria.length;

      return results;
    });

    // Evaluate results
    const score = [];
    if (accessibilityChecks.hasSkipLinks) score.push('Skip Links');
    if (accessibilityChecks.formLabelsRatio >= 0.8) score.push('Form Labels');
    if (accessibilityChecks.hasHeadings) score.push('Heading Structure');
    if (accessibilityChecks.ariaElements > 0) score.push('ARIA Attributes');

    console.log(`   ♿ Accessibility Features: ${score.join(', ') || 'None detected'}`);
    console.log(`   📝 Form Label Coverage: ${(accessibilityChecks.formLabelsRatio * 100).toFixed(0)}%`);

    return {
      url: url,
      features: score,
      formLabelsRatio: accessibilityChecks.formLabelsRatio,
      hasHeadings: accessibilityChecks.hasHeadings,
      ariaElements: accessibilityChecks.ariaElements,
      score: score.length
    };

  } catch (error) {
    console.log(`   ❌ Accessibility check failed: ${error.message}`);
    return { url: url, error: error.message, score: 0 };
  }
}

/**
 * Main health check runner
 */
async function runHealthCheck() {
  console.log('🏥 Starting CSS Health Check');
  console.log('============================\n');

  let browser;
  const healthReport = {
    timestamp: new Date().toISOString(),
    cssFiles: [],
    performance: [],
    accessibility: [],
    summary: {}
  };

  try {
    browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();

    // Check CSS files
    healthReport.cssFiles = await checkCSSFiles(page);

    // Check performance for each endpoint
    for (const endpoint of HEALTH_CHECK_ENDPOINTS) {
      const perfResult = await monitorLayoutShifts(page, endpoint);
      const a11yResult = await checkAccessibility(page, endpoint);
      
      healthReport.performance.push(perfResult);
      healthReport.accessibility.push(a11yResult);
    }

  } catch (error) {
    console.error('❌ Health check failed:', error);
    healthReport.error = error.message;
  } finally {
    if (browser) {
      await browser.close();
    }
  }

  // Generate summary
  generateHealthSummary(healthReport);
  
  // Save report
  const reportPath = path.join(__dirname, 'health-report.json');
  fs.writeFileSync(reportPath, JSON.stringify(healthReport, null, 2));

  console.log(`\n📄 Health report saved to: ${reportPath}`);

  // Exit with appropriate code
  const hasErrors = healthReport.cssFiles.some(f => !f.accessible) ||
                   healthReport.performance.some(p => !p.clsHealthy || !p.cssLoadHealthy);
  
  process.exit(hasErrors ? 1 : 0);
}

/**
 * Generate health summary
 */
function generateHealthSummary(report) {
  console.log('\n🏥 HEALTH CHECK SUMMARY');
  console.log('=======================');

  // CSS Files
  const accessibleFiles = report.cssFiles.filter(f => f.accessible).length;
  const totalFiles = report.cssFiles.length;
  console.log(`CSS Files: ${accessibleFiles}/${totalFiles} accessible`);

  // Performance
  const healthyPages = report.performance.filter(p => p.clsHealthy && p.cssLoadHealthy).length;
  const totalPages = report.performance.length;
  console.log(`Performance: ${healthyPages}/${totalPages} pages healthy`);

  // Accessibility
  const avgA11yScore = report.accessibility.reduce((sum, a) => sum + (a.score || 0), 0) / report.accessibility.length;
  console.log(`Accessibility: ${avgA11yScore.toFixed(1)}/4 average score`);

  // Overall status
  const overallHealthy = accessibleFiles === totalFiles && healthyPages === totalPages;
  console.log(`\nOverall Status: ${overallHealthy ? '✅ HEALTHY' : '⚠️  NEEDS ATTENTION'}`);

  report.summary = {
    cssFilesAccessible: `${accessibleFiles}/${totalFiles}`,
    performanceHealthy: `${healthyPages}/${totalPages}`,
    accessibilityScore: avgA11yScore,
    overallHealthy
  };
}

// Run health check if called directly
if (require.main === module) {
  runHealthCheck();
}

module.exports = { runHealthCheck, checkCSSFiles, monitorLayoutShifts }; 