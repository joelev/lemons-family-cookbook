/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        // Warm, inviting palette for a family cookbook
        cream: '#FDF8F3',
        ivory: '#FAF7F2',
        linen: '#F5F0E8',

        // Text hierarchy
        ink: '#2C2416',
        'ink-light': '#4A3F2F',
        'ink-muted': '#7A6F5F',

        // Warm accent - sienna/terracotta
        sienna: {
          DEFAULT: '#A0522D',
          light: '#C67B4E',
          dark: '#7A3E22',
        },

        // Cool accent - forest/sage
        sage: {
          DEFAULT: '#5F7161',
          light: '#8A9A8C',
          dark: '#3D4A3F',
        },

        // Utility
        rule: '#E8E2D9',
        'rule-dark': '#D4CCC0',
      },
      fontFamily: {
        display: ['Playfair Display', 'Georgia', 'serif'],
        body: ['Crimson Pro', 'Georgia', 'serif'],
        ui: ['Inter', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        // Fluid typography using clamp()
        'fluid-xs': ['clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem)', { lineHeight: '1.5' }],
        'fluid-sm': ['clamp(0.875rem, 0.8rem + 0.35vw, 1rem)', { lineHeight: '1.6' }],
        'fluid-base': ['clamp(1rem, 0.9rem + 0.5vw, 1.125rem)', { lineHeight: '1.7' }],
        'fluid-lg': ['clamp(1.125rem, 1rem + 0.6vw, 1.25rem)', { lineHeight: '1.6' }],
        'fluid-xl': ['clamp(1.25rem, 1.1rem + 0.75vw, 1.5rem)', { lineHeight: '1.5' }],

        // Display sizes - more dramatic scaling
        'display-sm': ['clamp(1.5rem, 1.2rem + 1.5vw, 2rem)', { lineHeight: '1.3' }],
        'display-md': ['clamp(1.875rem, 1.5rem + 1.875vw, 2.5rem)', { lineHeight: '1.2' }],
        'display-lg': ['clamp(2.25rem, 1.75rem + 2.5vw, 3.5rem)', { lineHeight: '1.15', letterSpacing: '-0.01em' }],
        'display-xl': ['clamp(3rem, 2rem + 5vw, 5rem)', { lineHeight: '1.1', letterSpacing: '-0.02em' }],
      },
      spacing: {
        // Content widths
        'content': '65ch',
        'content-wide': '75ch',

        // Section spacing
        'section-sm': 'clamp(2rem, 4vw, 3rem)',
        'section-md': 'clamp(3rem, 6vw, 5rem)',
        'section-lg': 'clamp(4rem, 8vw, 7rem)',

        // Component spacing
        'card': '1.5rem',
        'card-lg': '2rem',
      },
      maxWidth: {
        'prose': '65ch',
        'prose-wide': '75ch',
      },
      borderRadius: {
        'card': '0.5rem',
      },
      boxShadow: {
        'card': '0 1px 3px rgba(44, 36, 22, 0.08), 0 1px 2px rgba(44, 36, 22, 0.06)',
        'card-hover': '0 4px 6px rgba(44, 36, 22, 0.1), 0 2px 4px rgba(44, 36, 22, 0.06)',
      },
    },
  },
  plugins: [],
};
