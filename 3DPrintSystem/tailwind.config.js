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
    'space-apple-xl',

    // V0.dev color system classes
    'btn-v0-primary',
    'btn-v0-secondary',
    'btn-v0-success',
    'btn-v0-danger',
    'btn-v0-warning',
    'card-v0',
    'badge-v0-new',
    'badge-v0-status',
    'tab-v0-active',
    'tab-v0-inactive',
    'input-v0',
    'text-v0-primary',
    'text-v0-secondary',
    'text-v0-muted',
    'bg-v0-background',
    'bg-v0-card',
    'border-v0-border',
    // Status colors for job age
    'text-v0-green-600',
    'text-v0-yellow-600', 
    'text-v0-orange-600',
    'text-v0-red-600',
    // Action button colors
    'bg-v0-blue-100',
    'text-v0-blue-700',
    'bg-v0-green-100',
    'text-v0-green-700',
    'bg-v0-red-100',
    'text-v0-red-700',
    'bg-v0-purple-100',
    'text-v0-purple-700',
    'bg-v0-orange-100',
    'text-v0-orange-800'
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
        'system-yellow': '#FFCC00',

        // V0.DEV UI Color System (extracted from v0.dev generated design)
        'v0-background': '#ffffff',
        'v0-foreground': '#0a0a0a',
        'v0-card': '#ffffff',
        'v0-card-foreground': '#0a0a0a',
        'v0-popover': '#ffffff',
        'v0-popover-foreground': '#0a0a0a',
        'v0-primary': '#171717',
        'v0-primary-foreground': '#fafafa',
        'v0-secondary': '#f5f5f5',
        'v0-secondary-foreground': '#171717',
        'v0-muted': '#f5f5f5',
        'v0-muted-foreground': '#737373',
        'v0-accent': '#f5f5f5',
        'v0-accent-foreground': '#171717',
        'v0-destructive': '#ef4444',
        'v0-destructive-foreground': '#fafafa',
        'v0-border': '#e5e5e5',
        'v0-input': '#e5e5e5',
        'v0-ring': '#0a0a0a',

        // V0.DEV Status & Action Colors
        'v0-blue': {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',  // Primary blue
          600: '#2563eb',  // Active tab blue
          700: '#1d4ed8',  // Hover blue
          800: '#1e40af',
          900: '#1e3a8a'
        },

        'v0-gray': {
          50: '#f9fafb',   // Very light background
          100: '#f3f4f6',
          200: '#e5e7eb',  // Card borders, inactive tab borders
          300: '#d1d5db',
          400: '#9ca3af',
          500: '#6b7280',
          600: '#4b5563',
          700: '#374151',
          800: '#1f2937',
          900: '#111827'
        },

        'v0-green': {
          50: '#f0fdf4',
          100: '#dcfce7',  // Success button background
          200: '#bbf7d0',
          300: '#86efac',
          400: '#4ade80',
          500: '#10b981',  // Success icons
          600: '#059669',  // Job age < 24h
          700: '#047857',  // Success button text
          800: '#065f46',
          900: '#064e3b'
        },

        'v0-yellow': {
          50: '#fffbeb',
          100: '#fef3c7',
          200: '#fde68a',
          300: '#fcd34d',
          400: '#fbbf24',
          500: '#f59e0b',
          600: '#d97706',  // Job age 24-48h
          700: '#b45309',
          800: '#92400e',
          900: '#78350f'
        },

        'v0-orange': {
          50: '#fff7ed',
          100: '#fed7aa',  // NEW badge background
          200: '#fed7d7',
          300: '#fdba74',
          400: '#fb923c',  // Unreviewed job border
          500: '#f97316',  // Orange alerts
          600: '#ea580c',  // Job age 48-72h
          700: '#c2410c',
          800: '#9a3412',  // NEW badge text
          900: '#7c2d12'
        },

        'v0-red': {
          50: '#fef2f2',
          100: '#fee2e2',  // Danger button background
          200: '#fecaca',
          300: '#fca5a5',
          400: '#f87171',
          500: '#ef4444',  // Destructive color
          600: '#dc2626',  // Job age > 72h
          700: '#b91c1c',  // Danger button text
          800: '#991b1b',
          900: '#7f1d1d'
        },

        'v0-purple': {
          50: '#faf5ff',
          100: '#f3e8ff',  // Purple button background
          200: '#e9d5ff',
          300: '#d8b4fe',
          400: '#c084fc',
          500: '#a855f7',
          600: '#9333ea',
          700: '#7c3aed',  // Purple button text
          800: '#6b21a8',
          900: '#581c87'
        }
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

        // V0.dev Button Components
        '.btn-v0-primary': {
          backgroundColor: theme('colors.v0-blue.600'),
          color: 'white',
          padding: '12px 16px',
          borderRadius: '12px',
          fontWeight: '500',
          fontSize: '14px',
          lineHeight: '20px',
          transition: 'all 200ms',
          border: 'none',
          '&:hover': {
            backgroundColor: theme('colors.v0-blue.700'),
            boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
          }
        },

        '.btn-v0-success': {
          backgroundColor: theme('colors.v0-green.100'),
          color: theme('colors.v0-green.700'),
          padding: '8px 12px',
          borderRadius: '8px',
          fontWeight: '500',
          fontSize: '14px',
          lineHeight: '20px',
          transition: 'all 200ms',
          border: 'none',
          display: 'flex',
          alignItems: 'center',
          '&:hover': {
            backgroundColor: theme('colors.v0-green.200')
          }
        },

        '.btn-v0-danger': {
          backgroundColor: theme('colors.v0-red.100'),
          color: theme('colors.v0-red.700'),
          padding: '8px 12px',
          borderRadius: '8px',
          fontWeight: '500',
          fontSize: '14px',
          lineHeight: '20px',
          transition: 'all 200ms',
          border: 'none',
          display: 'flex',
          alignItems: 'center',
          '&:hover': {
            backgroundColor: theme('colors.v0-red.200')
          }
        },

        '.btn-v0-secondary': {
          backgroundColor: theme('colors.v0-blue.100'),
          color: theme('colors.v0-blue.700'),
          padding: '8px 12px',
          borderRadius: '8px',
          fontWeight: '500',
          fontSize: '14px',
          lineHeight: '20px',
          transition: 'all 200ms',
          border: 'none',
          display: 'flex',
          alignItems: 'center',
          '&:hover': {
            backgroundColor: theme('colors.v0-blue.200')
          }
        },

        '.btn-v0-warning': {
          backgroundColor: theme('colors.v0-purple.100'),
          color: theme('colors.v0-purple.700'),
          padding: '8px 12px',
          borderRadius: '8px',
          fontWeight: '500',
          fontSize: '14px',
          lineHeight: '20px',
          transition: 'all 200ms',
          border: 'none',
          display: 'flex',
          alignItems: 'center',
          '&:hover': {
            backgroundColor: theme('colors.v0-purple.200')
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
        },

        // V0.dev Card Components
        '.card-v0': {
          backgroundColor: theme('colors.v0-card'),
          borderRadius: '12px',
          border: '1px solid',
          borderColor: theme('colors.v0-gray.200'),
          boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
          transition: 'all 200ms',
          '&:hover': {
            boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
          }
        },

        '.card-v0-unreviewed': {
          backgroundColor: theme('colors.v0-card'),
          borderRadius: '12px',
          border: '1px solid',
          borderColor: theme('colors.v0-orange.400'),
          boxShadow: '0 1px 3px 0 rgba(251, 146, 60, 0.1)',
          transition: 'all 200ms'
        },

        // V0.dev Badge Components
        '.badge-v0-new': {
          backgroundColor: theme('colors.v0-orange.100'),
          color: theme('colors.v0-orange.800'),
          fontSize: '12px',
          fontWeight: '600',
          padding: '4px 8px',
          borderRadius: '9999px'
        },

        '.badge-v0-status': {
          fontSize: '12px',
          fontWeight: '600',
          padding: '4px 8px',
          borderRadius: '9999px'
        },

        // V0.dev Tab Components
        '.tab-v0-active': {
          backgroundColor: theme('colors.v0-blue.600'),
          color: 'white',
          padding: '12px 16px',
          borderRadius: '12px',
          border: '1px solid',
          borderColor: theme('colors.v0-blue.600'),
          fontWeight: '500',
          boxShadow: '0 2px 4px -1px rgba(0, 0, 0, 0.1)',
          transition: 'all 200ms'
        },

        '.tab-v0-inactive': {
          backgroundColor: theme('colors.v0-card'),
          color: theme('colors.v0-blue.600'),
          padding: '12px 16px',
          borderRadius: '12px',
          border: '1px solid',
          borderColor: theme('colors.v0-gray.200'),
          fontWeight: '500',
          transition: 'all 200ms',
          '&:hover': {
            backgroundColor: theme('colors.v0-blue.50'),
            boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)'
          }
        },

        // V0.dev Input Components
        '.input-v0': {
          backgroundColor: theme('colors.v0-card'),
          border: '1px solid',
          borderColor: theme('colors.v0-input'),
          borderRadius: '6px',
          padding: '8px 12px',
          fontSize: '14px',
          lineHeight: '20px',
          transition: 'all 200ms',
          '&:focus': {
            outline: 'none',
            borderColor: theme('colors.v0-ring'),
            boxShadow: '0 0 0 2px rgba(0, 0, 0, 0.05)'
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