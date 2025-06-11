/**
 * RESPONSIVE UI TESTING SUITE
 * 3D Print System - Automated UI Testing
 * 
 * Tests the responsive behavior across all device breakpoints
 * Specifically validates the tab scrolling fix and modal interactions
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

// Test configuration
const FLASK_URL = 'http://localhost:5000';
const BREAKPOINTS = [
  { name: 'mobile-portrait', width: 320, height: 568 },
  { name: 'mobile-landscape', width: 568, height: 320 },
  { name: 'tablet-portrait', width: 768, height: 1024 },
  { name: 'tablet-landscape', width: 1024, height: 768 },
  { name: 'desktop', width: 1440, height: 900 },
  { name: 'desktop-xl', width: 1920, height: 1080 },
];

const TEST_RESULTS = [];

/**
 * Test tab scrolling functionality
 */
async function testTabScrolling(page, breakpoint) {
  console.log(`\n🧪 Testing tab scrolling on ${breakpoint.name} (${breakpoint.width}x${breakpoint.height})`);
  
  try {
    // Navigate to dashboard
    await page.goto(`${FLASK_URL}/dashboard`, { 
      waitUntil: 'networkidle2',
      timeout: 10000 
    });

    // Wait for tabs to load
    await page.waitForSelector('.tabs-v0', { timeout: 5000 });
    
    // Get tab container element
    const tabContainer = await page.$('.tabs-v0');
    if (!tabContainer) {
      throw new Error('Tab container not found');
    }

    // Check scroll properties
    const scrollInfo = await tabContainer.evaluate(el => ({
      scrollWidth: el.scrollWidth,
      clientWidth: el.clientWidth,
      scrollLeft: el.scrollLeft,
      canScroll: el.scrollWidth > el.clientWidth
    }));

    console.log(`   📏 Container: ${scrollInfo.clientWidth}px, Content: ${scrollInfo.scrollWidth}px`);

    let testResult = {
      breakpoint: breakpoint.name,
      viewport: `${breakpoint.width}x${breakpoint.height}`,
      tabScrolling: {
        canScroll: scrollInfo.canScroll,
        scrollWidth: scrollInfo.scrollWidth,
        clientWidth: scrollInfo.clientWidth,
        status: 'PASS'
      }
    };

    // If content overflows, test scrolling
    if (scrollInfo.canScroll) {
      console.log(`   🔄 Testing horizontal scroll capability...`);
      
      // Test scroll right
      await tabContainer.evaluate(el => el.scrollLeft = 100);
      await page.waitForTimeout(500);
      
      const newScrollLeft = await tabContainer.evaluate(el => el.scrollLeft);
      
      if (newScrollLeft > 0) {
        console.log(`   ✅ Horizontal scroll working (scrolled to ${newScrollLeft}px)`);
        
        // Test scroll indicators (webkit scrollbar)
        const hasScrollbar = await page.evaluate(() => {
          const style = getComputedStyle(document.querySelector('.tabs-v0'));
          return style.overflowX === 'auto' || style.overflowX === 'scroll';
        });
        
        if (hasScrollbar) {
          console.log(`   ✅ Scroll indicators enabled`);
        } else {
          console.log(`   ⚠️  Scroll indicators may be hidden`);
        }
        
      } else {
        throw new Error('Horizontal scrolling not working');
      }
    } else {
      console.log(`   ✅ All tabs fit in container (no scrolling needed)`);
    }

    // Test individual tab interaction
    const tabs = await page.$$('.tab-v0-active, .tab-v0-inactive');
    if (tabs.length > 0) {
      console.log(`   🎯 Testing tab interaction (${tabs.length} tabs found)`);
      
      // Click first tab to test interaction
      await tabs[0].click();
      await page.waitForTimeout(300);
      
      console.log(`   ✅ Tab interaction working`);
      testResult.tabScrolling.interactionTest = 'PASS';
    }

    TEST_RESULTS.push(testResult);
    return testResult;

  } catch (error) {
    console.log(`   ❌ Tab scrolling test failed: ${error.message}`);
    
    const failResult = {
      breakpoint: breakpoint.name,
      viewport: `${breakpoint.width}x${breakpoint.height}`,
      tabScrolling: {
        status: 'FAIL',
        error: error.message
      }
    };
    
    TEST_RESULTS.push(failResult);
    return failResult;
  }
}

/**
 * Test modal interactions
 */
async function testModalInteractions(page, breakpoint) {
  console.log(`\n🪟 Testing modal interactions on ${breakpoint.name}`);
  
  try {
    // Look for modal trigger buttons
    const modalTriggers = await page.$$('[data-modal-trigger], .btn-v0-danger, .btn-v0-warning');
    
    if (modalTriggers.length === 0) {
      console.log(`   ℹ️  No modal triggers found - skipping modal test`);
      return { status: 'SKIPPED' };
    }

    // Test first modal trigger
    await modalTriggers[0].click();
    await page.waitForTimeout(500);

    // Check if modal appeared
    const modal = await page.$('#confirmation-modal, .modal, [role="dialog"]');
    
    if (modal) {
      console.log(`   ✅ Modal opened successfully`);
      
      // Test modal z-index and visibility
      const modalStyle = await modal.evaluate(el => {
        const computedStyle = getComputedStyle(el);
        const rect = el.getBoundingClientRect();
        return {
          zIndex: computedStyle.zIndex,
          display: computedStyle.display,
          visibility: computedStyle.visibility,
          isVisible: rect.width > 0 && rect.height > 0
        };
      });
      
      if (modalStyle.isVisible && modalStyle.zIndex >= 400) {
        console.log(`   ✅ Modal properly stacked (z-index: ${modalStyle.zIndex})`);
      } else {
        throw new Error(`Modal z-index issue (z-index: ${modalStyle.zIndex})`);
      }
      
      // Close modal (click backdrop or close button)
      const closeButton = await page.$('.modal-close, [data-modal-close]');
      if (closeButton) {
        await closeButton.click();
      } else {
        // Click backdrop
        await page.keyboard.press('Escape');
      }
      
      await page.waitForTimeout(300);
      console.log(`   ✅ Modal closed successfully`);
      
      return { status: 'PASS', zIndex: modalStyle.zIndex };
      
    } else {
      throw new Error('Modal did not appear after trigger click');
    }

  } catch (error) {
    console.log(`   ❌ Modal test failed: ${error.message}`);
    return { status: 'FAIL', error: error.message };
  }
}

/**
 * Test CSS loading and error detection
 */
async function testCSSLoading(page) {
  console.log(`\n🎨 Testing CSS loading and architecture...`);
  
  try {
    // Check if main.css loaded successfully
    const cssResponse = await page.goto(`${FLASK_URL}/static/css/main.css`);
    
    if (cssResponse.status() === 200) {
      console.log(`   ✅ main.css loaded successfully (${cssResponse.status()})`);
    } else {
      throw new Error(`CSS loading failed (${cssResponse.status()})`);
    }

    // Go back to dashboard
    await page.goto(`${FLASK_URL}/dashboard`, { waitUntil: 'networkidle2' });

    // Check if CSS variables are working
    const cssVariables = await page.evaluate(() => {
      const root = document.documentElement;
      const computedStyle = getComputedStyle(root);
      return {
        primaryColor: computedStyle.getPropertyValue('--color-primary').trim(),
        spacingMd: computedStyle.getPropertyValue('--spacing-md').trim(),
        radiusMd: computedStyle.getPropertyValue('--radius-md').trim()
      };
    });

    if (cssVariables.primaryColor && cssVariables.spacingMd) {
      console.log(`   ✅ CSS variables loaded (primary: ${cssVariables.primaryColor})`);
    } else {
      throw new Error('CSS variables not found - architecture may have issues');
    }

    // Check for CSS errors in console
    const consoleLogs = [];
    page.on('console', msg => {
      if (msg.type() === 'error' && msg.text().includes('css')) {
        consoleLogs.push(msg.text());
      }
    });

    await page.waitForTimeout(1000);

    if (consoleLogs.length === 0) {
      console.log(`   ✅ No CSS errors detected`);
    } else {
      console.log(`   ⚠️  CSS errors found: ${consoleLogs.join(', ')}`);
    }

    return { 
      status: 'PASS', 
      cssVariables, 
      errors: consoleLogs.length 
    };

  } catch (error) {
    console.log(`   ❌ CSS loading test failed: ${error.message}`);
    return { status: 'FAIL', error: error.message };
  }
}

/**
 * Main test runner
 */
async function runResponsiveTests() {
  console.log('🚀 Starting Responsive UI Testing Suite');
  console.log('=====================================\n');

  let browser;
  try {
    // Launch browser
    browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();

    // Test CSS loading first
    const cssTest = await testCSSLoading(page);
    
    if (cssTest.status === 'FAIL') {
      console.log('❌ CSS loading failed - aborting responsive tests');
      process.exit(1);
    }

    // Run tests for each breakpoint
    for (const breakpoint of BREAKPOINTS) {
      console.log(`\n📱 Testing breakpoint: ${breakpoint.name}`);
      console.log('='.repeat(50));

      // Set viewport
      await page.setViewport({
        width: breakpoint.width,
        height: breakpoint.height
      });

      // Run tab scrolling test
      await testTabScrolling(page, breakpoint);

      // Run modal interaction test  
      const modalResult = await testModalInteractions(page, breakpoint);
      
      // Add small delay between tests
      await page.waitForTimeout(1000);
    }

  } catch (error) {
    console.error('❌ Test suite failed:', error);
    process.exit(1);
  } finally {
    if (browser) {
      await browser.close();
    }
  }

  // Generate test report
  generateTestReport();
}

/**
 * Generate test report
 */
function generateTestReport() {
  console.log('\n📊 TEST RESULTS SUMMARY');
  console.log('========================');

  const summary = {
    total: TEST_RESULTS.length,
    passed: TEST_RESULTS.filter(r => r.tabScrolling?.status === 'PASS').length,
    failed: TEST_RESULTS.filter(r => r.tabScrolling?.status === 'FAIL').length
  };

  console.log(`Total Tests: ${summary.total}`);
  console.log(`Passed: ${summary.passed}`);
  console.log(`Failed: ${summary.failed}`);
  console.log(`Success Rate: ${((summary.passed / summary.total) * 100).toFixed(1)}%`);

  // Detailed results
  TEST_RESULTS.forEach(result => {
    const status = result.tabScrolling?.status === 'PASS' ? '✅' : '❌';
    console.log(`${status} ${result.breakpoint} (${result.viewport})`);
    
    if (result.tabScrolling?.status === 'FAIL') {
      console.log(`    Error: ${result.tabScrolling.error}`);
    }
  });

  // Save results to file
  const reportPath = path.join(__dirname, 'test-results.json');
  fs.writeFileSync(reportPath, JSON.stringify({
    timestamp: new Date().toISOString(),
    summary,
    results: TEST_RESULTS
  }, null, 2));

  console.log(`\n📄 Detailed report saved to: ${reportPath}`);

  // Exit with appropriate code
  process.exit(summary.failed === 0 ? 0 : 1);
}

// Run tests if called directly
if (require.main === module) {
  runResponsiveTests();
}

module.exports = { runResponsiveTests, testTabScrolling, testModalInteractions }; 