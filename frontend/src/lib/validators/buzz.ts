import { z } from 'zod';

export const BuzzValidator = z.object({
	name: z.string().min(3).max(21),
});

export const BuzzSubscriptionValidator = z.object({
	buzzId: z.string(),
});

export type CreateBuzzPayload = z.infer<typeof BuzzValidator>;
export type SubscribeToBuzzPayload = z.infer<typeof BuzzSubscriptionValidator>;
