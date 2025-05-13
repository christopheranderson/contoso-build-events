import { Box, Flex, Icon, useBreakpointValue, } from "@chakra-ui/react"
import { Link, useParams } from "@tanstack/react-router"
import {GoCalendar} from "react-icons/go"

import {ColorModeButton} from "@/components/ui/color-mode"

import UserMenu from "./UserMenu"

function Crumb() {
  const params = useParams({ strict: false })
  return (
    <Box pt="1.5" >
      <Box as="span" textDecoration="underline">
      <Link to={`/${params.org_slug}`} >
        {params.org_slug}
      </Link>
      </Box>
      
      {params.event_slug && (
        <>
          <Box as="span" mx={2}>
            /
          </Box>
          <Box as="span" textDecoration="underline">
          <Link to={`/${params.org_slug}/${params.event_slug}`}>
            {params.event_slug}
          </Link>
          </Box>
        </>
      )}
    </Box>
  )
}

function Navbar() {
  const display = useBreakpointValue({ base: "none", md: "flex" })
  
  return (
    <Flex
      display={display}
      justify="space-between"
      position="sticky"
      align="center"
      bg="bg.muted"
      w="100%"
      top={0}
      p={4}
    >
      <Flex align="center">
        <Box mr={"6"} fontSize="2xl" fontWeight="bold" letterSpacing={"tight"}>
          <Link to="/" >
            <Icon as={GoCalendar} mb="1" /> BuildEvents
          </Link>
        </Box>
        <Crumb />
      </Flex>
      <Flex gap={2} alignItems="center">
        <ColorModeButton />
        <UserMenu />
      </Flex>
    </Flex>
  )
}

export default Navbar
