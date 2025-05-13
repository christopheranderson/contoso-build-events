import { Flex } from "@chakra-ui/react"
import { Outlet, createFileRoute, redirect } from "@tanstack/react-router"

export const Route = createFileRoute("/_auth/_base")({
  component: BaseLayout,
})

function BaseLayout() {
  return (
    <Flex flex="1" direction="column" p={4} overflowY="auto">
        <Outlet />
    </Flex>
  )
}

export default BaseLayout
