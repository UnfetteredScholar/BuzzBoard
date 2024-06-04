import { getAuthSession } from '@/lib/auth';
import { db } from '@/lib/db';
import { BuzzValidator } from '@/lib/validators/buzz';
import { z } from 'zod';

export async function POST(req: Request) {
	try {
		const session = await getAuthSession();

		if (!session?.user) {
			return new Response('Unauthorized', { status: 401 });
		}

		const body = await req.json();
		const { name } = BuzzValidator.parse(body);

		// check if buzz already exists
		const buzzExists = await db.buzz.findFirst({
			where: {
				name,
			},
		});

		if (buzzExists) {
			return new Response('Buzz already exists', { status: 409 });
		}

		// create subreddit and associate it with the user
		const buzz = await db.buzz.create({
			data: {
				name,
				creatorId: session.user.id,
			},
		});

		// creator also has to be subscribed
		await db.subscription.create({
			data: {
				userId: session.user.id,
				buzzId: buzz.id,
			},
		});

		return new Response(buzz.name);
	} catch (error) {
		if (error instanceof z.ZodError) {
			return new Response(error.message, { status: 422 });
		}

		return new Response('Could not create buzz', { status: 500 });
	}
}
