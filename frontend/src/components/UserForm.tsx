'use client';

import { FC, useState } from 'react';
import { Button } from './ui/Button';
import { cn } from '@/lib/utils';
import { signIn } from 'next-auth/react';
import { Icons } from './Icons';
import { useToast } from '@/hooks/use-toast';
import { useForm, SubmitHandler } from 'react-hook-form';

interface FieldValues {
	email: string;
	username: string;
	password: string;
}

interface UserFormProps extends React.HTMLAttributes<HTMLDivElement> {}

const UserForm: FC<UserFormProps> = ({ className, ...props }) => {
	const [isLoading, setIsLoading] = useState<boolean>(false);
	const { toast } = useToast();

	const {
		register,
		handleSubmit,
		formState: { errors },
	} = useForm<FieldValues>();

	const onSubmit: SubmitHandler<FieldValues> = async (data) => {
		setIsLoading(true);

		try {
			const response = await fetch('/api/auth/signup', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(data),
			});

			const result = await response.json();

			if (!response.ok) {
				throw new Error(result.message || 'Something went wrong!');
			}

			toast({
				title: 'Sign Up Successful',
				description: 'You can now log in with your credentials',
				// variant: 'success',
			});
		} catch (error) {
			toast({
				title: 'Sign Up Failed',
				description: (error as Error).message,
				variant: 'destructive',
			});
		} finally {
			setIsLoading(false);
		}
	};

	const loginWithGoogle = async () => {
		setIsLoading(true);

		try {
			await signIn('google');
		} catch (error) {
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
				<form onSubmit={handleSubmit(onSubmit)}>
					<div className="mb-4">
						<label
							htmlFor="email"
							className="block text-left text-sm font-medium text-gray-700"
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
							htmlFor="username"
							className="block text-left text-sm font-medium text-gray-700"
						>
							Username
						</label>
						<input
							type="text"
							id="username"
							{...register('username', { required: 'Username is required' })}
							className="w-full px-3 py-2 rounded-md border border-gray-300 focus:outline-none focus:ring-1 focus:ring-blue-500"
							placeholder="Enter your username"
						/>
						{errors.username && (
							<span className="text-red-500 text-sm">
								{errors.username.message}
							</span>
						)}
					</div>
					<div className="mb-4">
						<label
							htmlFor="password"
							className="block text-left text-sm font-medium text-gray-700"
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

export default UserForm;
