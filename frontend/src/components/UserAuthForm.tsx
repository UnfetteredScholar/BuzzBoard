'use client';

import { FC, useState } from 'react';
import { Button } from './ui/Button';
import { cn } from '@/lib/utils';
import { signIn } from 'next-auth/react';
import { Icons } from './Icons';
import { useToast } from '@/hooks/use-toast';
import { useForm } from 'react-hook-form';

interface FieldValues {
	email: string;
	password: string;
}

interface UserAuthFormProps extends React.HTMLAttributes<HTMLDivElement> {}

const UserAuthForm: FC<UserAuthFormProps> = ({ className, ...props }) => {
	const [isLoading, setIsLoading] = useState<boolean>(false);
	const { toast } = useToast();

	const {
		register,
		handleSubmit,
		formState: { errors },
	} = useForm<FieldValues>();

	const onSubmit = async (data: FieldValues) => {
		setIsLoading(true);

		try {
			// Replace with your actual sign up logic using data.email and data.password
			console.log(
				'Sign up with email:',
				data.email,
				'and password:',
				data.password
			);
			// You can use next-auth/react for sign up if applicable
			// await signUp('email', data);
		} catch (error) {
			console.error('Error during sign up:', error);
			// Handle sign up errors here (e.g., display toast notification)
		} finally {
			setIsLoading(false);
		}
	};

	const loginWithGoogle = async () => {
		setIsLoading(true);

		try {
			throw new Error();
			await signIn('google');
		} catch (error) {
			//toast notification
			toast({
				title: 'Oops!',
				description: 'Working on this feature. Come back later',
				variant: 'destructive',
			});
		} finally {
			setIsLoading(false);
		}
	};

	return (
		<div className={cn('flex justify-center', className)} {...props}>
			<div className="flex flex-col items-center">
				{/* Sign up form */}
				<form onSubmit={handleSubmit(onSubmit)}>
					<div className="mb-4">
						<label
							htmlFor="email"
							className="block text-sm font-medium text-gray-700"
						>
							Email Address
						</label>
						<input
							type="email"
							id="email"
							{...register('email', { required: 'Email is required' })}
							className="w-full px-3 py-2 rounded-md border border-gray-300 focus:outline-none focus:ring-1 focus:ring-blue-500"
							placeholder="Enter your email"
						/>
						{errors.email && (
							<span className="text-red-500 text-sm">
								{errors.email.message}
							</span>
						)}
					</div>
					<div className="mb-4">
						<label
							htmlFor="password"
							className="block text-sm font-medium text-gray-700"
						>
							Password
						</label>
						<input
							type="password"
							id="password"
							{...register('password', { required: 'Password is required' })}
							className="w-full px-3 py-2 rounded-md border border-gray-300 focus:outline-none focus:ring-1 focus:ring-blue-500"
							placeholder="Enter your password"
						/>
						{errors.password && (
							<span className="text-red-500 text-sm">
								{errors.password.message}
							</span>
						)}
					</div>
					<Button
						type="submit"
						isLoading={isLoading}
						size="sm"
						className="w-full"
					>
						Sign Up
					</Button>
				</form>

				<p className="mt-4 text-sm max-w-xs mx-auto">or</p>

				<Button
					isLoading={isLoading}
					onClick={loginWithGoogle}
					size="sm"
					className="w-full mt-4"
				>
					{isLoading ? null : <Icons.google className="h-4 w-4 mr-2" />}
					Google
				</Button>
			</div>
		</div>
	);
};

export default UserAuthForm;
