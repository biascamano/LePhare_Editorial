import { defineConfig } from 'astro/config';

export default defineConfig({
  site: process.env.PHARE_SITE ?? 'https://test.le-phare.info',
  trailingSlash: 'always',
  build: { format: 'directory' },
  output: 'static',
});
