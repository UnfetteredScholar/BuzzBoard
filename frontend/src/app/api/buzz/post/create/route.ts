import { getAuthSession } from '@/lib/auth';
import { db } from '@/lib/db';
import { PostValidator } from '@/lib/validators/post';
import { z } from 'zod';

export async function POST(req: Request) {
	try {
		const body = await req.json();

		const { title, content, buzzId } = PostValidator.parse(body);

		const session = await getAuthSession();

		if (!session?.user) {
			return new Response('Unauthorized', { status: 401 });
		}

		// verify user is subscribed to passed buzz id
		const subscription = await db.subscription.findFirst({
			where: {
				buzzId,
				userId: session.user.id,
			},
		});

		if (!subscription) {
			return new Response('Subscribe to post', { status: 403 });
		}

		await db.post.create({
			data: {
				title,
				content,
				authorId: session.user.id,
				buzzId,
			},
		});

		return new Response('OK');
	} catch (error) {
		if (error instanceof z.ZodError) {
			return new Response(error.message, { status: 400 });
		}

		return new Response(
			'Could not post to buzz at this time. Please try later',
			{ status: 500 }
		);
	}
}
