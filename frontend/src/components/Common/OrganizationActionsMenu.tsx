import { IconButton } from "@chakra-ui/react"
import { BsThreeDotsVertical } from "react-icons/bs"
import { MenuContent, MenuRoot, MenuTrigger } from "../ui/menu"

import type { Organization } from "@/client"
// import DeleteOrganization from "../Organizations/DeleteOrganization"
import EditOrganization from "../Organizations/Edit"

interface OrganizationActionMenuProps {
  organization: Organization
}

export const OrganizationActionsMenu = ({ organization }: OrganizationActionMenuProps) => {
  return (
    <MenuRoot>
      <MenuTrigger asChild>
        <IconButton variant="ghost" color="inherit">
          <BsThreeDotsVertical />
        </IconButton>
      </MenuTrigger>
      <MenuContent>
        <EditOrganization organization={organization} />
        {/* <DeleteOrganization id={organization.id!} /> */}
      </MenuContent>
    </MenuRoot>
  )
}
