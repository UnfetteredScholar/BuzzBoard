import { User } from 'next-auth';
import { FC } from 'react';
import { DropdownMenu, DropdownMenuTrigger } from './ui/DropdownMenu';
import UserAvatar from './UserAvatar';

interface UserAccountNavProps {
	user: Pick<User, 'name' | 'image' | 'email'>;
}

const UserAccountNav: FC<UserAccountNavProps> = ({ user }) => {
	return (
		<DropdownMenu>
			<DropdownMenuTrigger>
				<UserAvatar user={user} />
			</DropdownMenuTrigger>
		</DropdownMenu>
	);
};

export default UserAccountNav;
