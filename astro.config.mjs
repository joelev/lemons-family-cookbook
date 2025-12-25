import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://joelev.github.io',
  base: '/lemons-family-cookbook/',
  integrations: [tailwind()],
  output: 'static',
});
