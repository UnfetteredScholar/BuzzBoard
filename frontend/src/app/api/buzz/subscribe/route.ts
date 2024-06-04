import { getAuthSession } from '@/lib/auth';
import { db } from '@/lib/db';
import { BuzzSubscriptionValidator } from '@/lib/validators/buzz';
import { z } from 'zod';

export async function POST(req: Request) {
	try {
		const session = await getAuthSession();

		if (!session?.user) {
			return new Response('Unauthorized', { status: 401 });
		}

		const body = await req.json();
		const { buzzId } = BuzzSubscriptionValidator.parse(body);

		// check if user has already subscribed to buzz
		const subscriptionExists = await db.subscription.findFirst({
			where: {
				buzzId,
				userId: session.user.id,
			},
		});

		if (subscriptionExists) {
			return new Response("You've already subscribed to this buzz", {
				status: 400,
			});
		}

		// create buzz and associate it with the user
		await db.subscription.create({
			data: {
				buzzId,
				userId: session.user.id,
			},
		});

		return new Response(buzzId);
	} catch (error) {
		error;
		if (error instanceof z.ZodError) {
			return new Response(error.message, { status: 400 });
		}

		return new Response(
			'Could not subscribe to buzz at this time. Please try later',
			{ status: 500 }
		);
	}
}
