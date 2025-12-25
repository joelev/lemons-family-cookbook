import { defineCollection, z } from 'astro:content';

const recipes = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    category: z.enum([
      'cakes-pies-frostings',
      'candies-cookies-confections',
      'main-dishes-meats-vegetables',
      'quickbreads-muffins-pancakes',
      'salads',
      'yeast-breads-rolls-sweet-dough',
    ]),
    story: z.string().optional(),
  }),
});

export const collections = { recipes };
