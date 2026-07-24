import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// The "writing" collection: one Markdown file per post in src/content/writing/.
// See the README for the non-developer guide to adding a post.
const writing = defineCollection({
  // Files starting with "_" are ignored, so you can stash notes/scratch files.
  loader: glob({ pattern: '**/[^_]*.md', base: './src/content/writing' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      pubDate: z.coerce.date(),
      description: z.string(),
      // Set to true to keep a post hidden from the site until it's ready.
      draft: z.boolean().default(false),
      // Optional 16:9 header image (put the file in src/assets/images/ and
      // reference it here, e.g. heroImage: ../../assets/images/my-photo.jpg).
      heroImage: image().optional(),
      heroAlt: z.string().optional(),
    }),
});

export const collections = { writing };
