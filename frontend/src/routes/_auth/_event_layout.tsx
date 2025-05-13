import { Flex, Tabs, For, VStack } from "@chakra-ui/react"
import { Outlet, createFileRoute, Link, LinkOptions, useLocation, linkOptions, useParams } from "@tanstack/react-router"
import {GoCalendar, GoMegaphone, GoPerson, GoGift, GoProjectRoadmap, GoGear} from "react-icons/go"

export const Route = createFileRoute('/_auth/_event_layout')({
  component: EventLayout
})


function EventLayout() {
    const {href, pathname} = useLocation()
    const params = useParams({ strict: false })
    const basePath = `/${params.org_slug}/${params.event_slug}`
  return (
    <>
        <Flex align="center"
        bg="bg.muted"
        w="100%"
        top={0}
        p={0}>
            <Tabs.Root defaultValue={href} orientation="horizontal" variant="line" width="full" ml="4">
                <Tabs.List>
                    <For each={[
                        linkOptions({
                            to: `${basePath}`,
                            label: "Overview",
                            icon: GoCalendar,
                        }),
                        linkOptions({
                            to: `${basePath}/sessions`,
                            label: "Sessions",
                            icon: GoProjectRoadmap,
                        }),
                        linkOptions({
                            to: `${basePath}/attendees`,
                            label: "Attendees",
                            icon: GoPerson,
                        }),
                        linkOptions({
                            to: `${basePath}/speakers`,
                            label: "Speakers",
                            icon: GoMegaphone,
                        }),
                        linkOptions({
                            to: `${basePath}/sponsors`,
                            label: "Sponsors",
                            icon: GoGift,
                        }),
                        linkOptions({
                            to: `${basePath}/settings`,
                            label: "Settings",
                            icon: GoGear,
                        })
                    ]}>
                        {(link) =>
                            <Tabs.Trigger value={link.to} key={link.to} asChild>
                                
                                <Link 
                                    to={link.to}
                                    className={href === link.to ? "active" : ""}
                                    key={"link" + link.to}
                                >
                                    <link.icon size={20} />
                                    {link.label}
                                </Link>
                            </Tabs.Trigger>
                        }
                    </For>
                    <Tabs.Indicator roundedTop={"md"}/>
                </Tabs.List>
            </Tabs.Root>
        </Flex>
        <Flex flex="1" overflow="hidden" justify="center">
            <VStack>
                <Outlet />
            </VStack>
        </Flex>
    </>
  )
}

export default EventLayout
