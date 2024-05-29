import Link from 'next/link';
import { Icons } from './Icons';
import UserForm from './UserForm';

const SignUp = () => {
	return (
		<div className="container mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[400px]">
			<div className="flex flex-col space-y-2 text-center">
				<Icons.logo className="mx-auto h-6 w-6" />
				<h1 className="text-2xl font-semibold tracking-tight">Hey There!</h1>
				<p className="text-sm max-w-xs mx-auto">
					Continuing means creating a BuzzBoard account. You'll also be agreeing
					to our terms (User Agreement and Privacy Policies).
				</p>

				{/* Sign Up Form */}
				<UserForm />

				<p className="px-8 text-center text-sm text-zinc-700">
					Already have an account?{' '}
					<Link
						href="/sign-in"
						className="hover:text-zinc-800 text-sm underline underline-offset-4"
					>
						Sign In
					</Link>
				</p>
			</div>
		</div>
	);
};

export default SignUp;
