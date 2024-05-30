import { NextApiRequest, NextApiResponse } from 'next';
import { hashPassword } from '../../../lib/auth';
import { createUser, findUserByEmail } from '../../../lib/user';

export default async function handler(
	req: NextApiRequest,
	res: NextApiResponse
) {
	if (req.method !== 'POST') {
		return res.status(405).end();
	}

	const { email, username, password } = req.body;

	if (
		!email ||
		!email.includes('@') ||
		!username ||
		!password ||
		password.trim().length < 7
	) {
		res.status(422).json({ message: 'Invalid input.' });
		return;
	}

	const existingUser = await findUserByEmail(email);
	if (existingUser) {
		res.status(422).json({ message: 'User exists already!' });
		return;
	}

	const hashedPassword = await hashPassword(password);
	const newUser = await createUser({
		email,
		username,
		password: hashedPassword,
	});

	res.status(201).json({ message: 'User created!', user: newUser });
}
