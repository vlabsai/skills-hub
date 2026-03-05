// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  site: process.env.SITE_URL,
  base: process.env.BASE_PATH || '/',
  output: 'static',
  trailingSlash: 'always',
  build: {
    assets: 'assets'
  }
});
