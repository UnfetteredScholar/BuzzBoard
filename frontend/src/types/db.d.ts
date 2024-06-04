import type { Post, Buzz, User, Vote, Comment } from '@prisma/client';

export type ExtendedPost = Post & {
	buzz: Buzz;
	votes: Vote[];
	author: User;
	comments: Comment[];
};
