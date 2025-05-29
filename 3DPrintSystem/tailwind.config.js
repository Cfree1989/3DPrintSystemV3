/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/static/**/*.js",
  ],
  safelist: [
    // Ensure our Apple components are always included
    'btn-apple-primary',
    'btn-apple-destructive', 
    'btn-apple-secondary',
    'btn-apple-text',
    'input-apple',
    'select-apple',
    'label-apple',
    'card-apple',
    'card-apple-glass',
    'nav-apple',
    'alert-apple',
    'alert-apple-warning',
    'alert-apple-error',
    'alert-apple-success',
    'form-group-apple',
    'glass',
    'glass-dark',
    'glass-strong',
    'touch-target',
    'touch-target-lg',
    'text-apple-large-title',
    'text-apple-title1',
    'text-apple-title2',
    'text-apple-title3',
    'text-apple-headline',
    'text-apple-body',
    'text-apple-callout',
    'text-apple-footnote',
    'space-apple-xs',
    'space-apple-sm',
    'space-apple',
    'space-apple-md',
    'space-apple-lg',
    'space-apple-xl'
  ],
  darkMode: 'class',
  theme: {
    extend: {
      // Apple SF Pro Font Stack
      fontFamily: {
        'sans': [
          'SF Pro Text',
          'SF Pro Display', 
          '-apple-system',
          'BlinkMacSystemFont',
          'system-ui',
          'Segoe UI',
          'Roboto',
          'Helvetica Neue',
          'Arial',
          'sans-serif'
        ],
        'mono': [
          'SF Mono',
          'Monaco',
          'Inconsolata',
          'Roboto Mono',
          'source-code-pro',
          'Menlo',
          'monospace'
        ]
      },
      
      // 8-Point Grid System (Apple Standard)
      spacing: {
        '0.5': '2px',   // 0.25 * 8pt
        '1': '4px',     // 0.5 * 8pt  
        '1.5': '6px',   // 0.75 * 8pt
        '2': '8px',     // 1 * 8pt
        '3': '12px',    // 1.5 * 8pt
        '4': '16px',    // 2 * 8pt
        '5': '20px',    // 2.5 * 8pt
        '6': '24px',    // 3 * 8pt
        '8': '32px',    // 4 * 8pt
        '10': '40px',   // 5 * 8pt
        '12': '48px',   // 6 * 8pt
        '16': '64px',   // 8 * 8pt
        '20': '80px',   // 10 * 8pt
        '24': '96px',   // 12 * 8pt
        // Apple minimum touch target: 44pt = 44px
        'touch': '44px',
        'touch-lg': '48px'
      },

      // Apple Color System with Purpose-Driven Colors
      colors: {
        // Apple Blue (Primary Actions)
        'apple-blue': {
          50: '#eff6ff',
          100: '#dbeafe', 
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6', // Primary blue
          600: '#007AFF', // Apple system blue
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a'
        },
        
        // Apple Red (Destructive Actions)
        'apple-red': {
          50: '#fef2f2',
          100: '#fee2e2',
          200: '#fecaca', 
          300: '#fca5a5',
          400: '#f87171',
          500: '#ef4444',
          600: '#FF3B30', // Apple system red
          700: '#dc2626',
          800: '#b91c1c',
          900: '#991b1b'
        },

        // Apple Green (Success)
        'apple-green': {
          50: '#f0fdf4',
          100: '#dcfce7',
          200: '#bbf7d0',
          300: '#86efac', 
          400: '#4ade80',
          500: '#22c55e',
          600: '#34C759', // Apple system green
          700: '#15803d',
          800: '#166534',
          900: '#14532d'
        },

        // Apple Gray System
        'apple-gray': {
          50: '#f9fafb',
          100: '#f3f4f6',
          200: '#e5e7eb',
          300: '#d1d5db',
          400: '#9ca3af',
          500: '#6b7280',
          600: '#4b5563',
          700: '#374151',
          800: '#1f2937',
          900: '#111827'
        },

        // Apple Orange (Warnings)
        'apple-orange': {
          600: '#FF9500'
        },

        // Apple System Colors
        'system-blue': '#007AFF',
        'system-red': '#FF3B30', 
        'system-green': '#34C759',
        'system-orange': '#FF9500',
        'system-yellow': '#FFCC00'
      },

      // Apple-style Border Radius
      borderRadius: {
        'apple': '8px',
        'apple-lg': '12px', 
        'apple-xl': '16px',
        'apple-2xl': '20px'
      },

      // Apple Multi-layered Shadows
      boxShadow: {
        'apple-sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        'apple': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
        'apple-md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'apple-lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'apple-xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        'apple-2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
        // Glassmorphism shadows
        'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
        'glass-lg': '0 8px 32px 0 rgba(31, 38, 135, 0.5)'
      },

      // Apple Typography Scale
      fontSize: {
        'apple-caption2': ['11px', { lineHeight: '13px', fontWeight: '400' }],
        'apple-caption1': ['12px', { lineHeight: '16px', fontWeight: '400' }], 
        'apple-footnote': ['13px', { lineHeight: '18px', fontWeight: '400' }],
        'apple-subheadline': ['15px', { lineHeight: '20px', fontWeight: '400' }],
        'apple-callout': ['16px', { lineHeight: '21px', fontWeight: '400' }],
        'apple-body': ['17px', { lineHeight: '22px', fontWeight: '400' }],
        'apple-headline': ['17px', { lineHeight: '22px', fontWeight: '600' }],
        'apple-title3': ['20px', { lineHeight: '25px', fontWeight: '400' }],
        'apple-title2': ['22px', { lineHeight: '28px', fontWeight: '400' }],
        'apple-title1': ['28px', { lineHeight: '34px', fontWeight: '400' }],
        'apple-large-title': ['34px', { lineHeight: '41px', fontWeight: '400' }]
      },

      // Backdrop Blur for Glassmorphism
      backdropBlur: {
        'apple': '10px',
        'apple-md': '16px',
        'apple-lg': '24px'
      },

      // Animation/Transition Timing (Apple-style)
      transitionTimingFunction: {
        'apple': 'cubic-bezier(0.25, 0.1, 0.25, 1)',
        'apple-spring': 'cubic-bezier(0.175, 0.885, 0.32, 1.275)'
      },

      transitionDuration: {
        'apple-fast': '150ms',
        'apple-normal': '200ms', 
        'apple-slow': '300ms'
      }
    }
  },
  plugins: [
    // Custom Apple Component Utilities
    function({ addUtilities, addComponents, theme }) {
      // Apple Touch Target Utilities
      addUtilities({
        '.touch-target': {
          minWidth: theme('spacing.touch'),
          minHeight: theme('spacing.touch'),
        },
        '.touch-target-lg': {
          minWidth: theme('spacing.touch-lg'),
          minHeight: theme('spacing.touch-lg'),
        }
      });

      // Glassmorphism Utilities
      addUtilities({
        '.glass': {
          background: 'rgba(255, 255, 255, 0.25)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.18)',
        },
        '.glass-dark': {
          background: 'rgba(0, 0, 0, 0.25)', 
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
        },
        '.glass-strong': {
          background: 'rgba(255, 255, 255, 0.4)',
          backdropFilter: 'blur(16px)',
          border: '1px solid rgba(255, 255, 255, 0.2)',
        }
      });

      // Apple Button Components
      addComponents({
        '.btn-apple-primary': {
          backgroundColor: theme('colors.apple-blue.600'),
          color: 'white',
          padding: `${theme('spacing.3')} ${theme('spacing.6')}`,
          borderRadius: theme('borderRadius.apple'),
          fontWeight: '600',
          minWidth: theme('spacing.touch'),
          minHeight: theme('spacing.touch'),
          fontSize: theme('fontSize.apple-body')[0],
          lineHeight: theme('fontSize.apple-body')[1].lineHeight,
          transition: 'all 200ms cubic-bezier(0.25, 0.1, 0.25, 1)',
          '&:hover': {
            backgroundColor: theme('colors.apple-blue.700'),
            transform: 'translateY(-1px)',
            boxShadow: theme('boxShadow.apple-lg')
          },
          '&:active': {
            transform: 'translateY(0)',
            boxShadow: theme('boxShadow.apple')
          }
        },
        '.btn-apple-destructive': {
          backgroundColor: theme('colors.apple-red.600'),
          color: 'white',
          padding: `${theme('spacing.3')} ${theme('spacing.6')}`,
          borderRadius: theme('borderRadius.apple'),
          fontWeight: '600',
          minWidth: theme('spacing.touch'),
          minHeight: theme('spacing.touch'),
          fontSize: theme('fontSize.apple-body')[0],
          lineHeight: theme('fontSize.apple-body')[1].lineHeight,
          transition: 'all 200ms cubic-bezier(0.25, 0.1, 0.25, 1)',
          '&:hover': {
            backgroundColor: theme('colors.apple-red.700'),
            transform: 'translateY(-1px)',
            boxShadow: theme('boxShadow.apple-lg')
          }
        },
        '.input-apple': {
          padding: `${theme('spacing.3')} ${theme('spacing.4')}`,
          borderRadius: theme('borderRadius.apple'),
          border: '1px solid',
          borderColor: theme('colors.apple-gray.300'),
          fontSize: theme('fontSize.apple-body')[0],
          lineHeight: theme('fontSize.apple-body')[1].lineHeight,
          minHeight: theme('spacing.touch'),
          transition: 'all 200ms cubic-bezier(0.25, 0.1, 0.25, 1)',
          '&:focus': {
            outline: 'none',
            borderColor: theme('colors.apple-blue.600'),
            boxShadow: `0 0 0 3px ${theme('colors.apple-blue.600')}20`,
            transform: 'translateY(-1px)'
          }
        }
      });
    }
  ],
  // Support for reduced motion accessibility
  corePlugins: {
    preflight: false, // We'll add our own preflight
  }
} 