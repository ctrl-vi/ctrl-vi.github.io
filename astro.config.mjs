// @ts-check
import { defineConfig } from 'astro/config';
import partytown from '@astrojs/partytown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import { fileURLToPath } from 'node:url';

import mdx from '@astrojs/mdx';

// https://astro.build/config
export default defineConfig({
  site: 'https://ctrl-vi.github.io',
  integrations: [partytown(), mdx()],
  vite: {
    resolve: {
      alias: {
        '@components': fileURLToPath(new URL('./src/components', import.meta.url)),
        '@assets': fileURLToPath(new URL('./src/assets', import.meta.url)),
        '@cardIcons': fileURLToPath(new URL('./src/assets/cardIcons', import.meta.url)),
        '@public': fileURLToPath(new URL('./public', import.meta.url)),
        '@styles': fileURLToPath(new URL('./src/styles', import.meta.url))
      }
    }
  },
  markdown: {
    syntaxHighlight: "prism",
    remarkPlugins: [remarkMath],
    rehypePlugins: [rehypeKatex]
  }
});