// @ts-check
import { defineConfig } from 'astro/config';
import partytown from '@astrojs/partytown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

import mdx from '@astrojs/mdx';

// https://astro.build/config
export default defineConfig({
  site: 'https://ctrl-vi.github.io',
  integrations: [partytown(), mdx()],
  markdown: {
    syntaxHighlight: "prism",
    remarkPlugins: [remarkMath],
    rehypePlugins: [rehypeKatex]
  }
});