import { glob } from "astro/loaders";
import { defineCollection, z } from "astro:content";

const projects = defineCollection({
    loader: glob({ pattern: "**/*.md", base: "./src/pages/projects" }),
    schema: ( {image} ) => z.object({
        article: z.object({
            publishedTime: z.coerce.date(),
            modifiedTime: z.coerce.date(),
            authors: z.array(z.string()),
            section: z.string(),
            tags: z.array(z.string())
        }),
        layout: z.string(),
        title: z.string(),
        description: z.string(),
        seoDescription: z.string(),
        image: z.object({
            src: image(),
            alt: z.string()
        }),
        startDate: z.coerce.date(),
        finishDate: z.coerce.date().optional(),
        tags: z.array(z.string())
    }),
});

export const collections = { projects };