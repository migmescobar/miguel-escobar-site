import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// The "thoughts" collection: one Markdown file per post in src/content/thoughts/.
// See the README for the non-developer guide to adding a post.
const thoughts = defineCollection({
  // Files starting with "_" are ignored, so you can stash notes/scratch files.
  loader: glob({ pattern: '**/[^_]*.md', base: './src/content/thoughts' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      // Optional distinct headline for the Thoughts list (falls back to `title`
      // if omitted). Lets a post's on-page headline differ from how it's
      // billed in the index, like a magazine's contents-page line vs. the
      // article's own head.
      listTitle: z.string().optional(),
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

export const collections = { thoughts };
