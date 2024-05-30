import { User } from 'next-auth';
import { FC } from 'react';
import { DropdownMenu, DropdownMenuTrigger } from './ui/DropdownMenu';

interface UserAccountNavProps {
	user: Pick<User, 'name' | 'image' | 'email'>;
}

const UserAccountNav: FC<UserAccountNavProps> = ({ user }) => {
	return (
		<DropdownMenu>
			<DropdownMenuTrigger></DropdownMenuTrigger>
		</DropdownMenu>
	);
};

export default UserAccountNav;
