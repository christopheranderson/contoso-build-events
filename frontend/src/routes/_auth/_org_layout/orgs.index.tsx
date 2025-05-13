import {
  Container,
  EmptyState,
  Flex,
  Heading,
  Table,
  VStack,
} from "@chakra-ui/react"
import { useQuery } from "@tanstack/react-query"
import { createFileRoute, useNavigate } from "@tanstack/react-router"
import { FiSearch } from "react-icons/fi"
import { z } from "zod"

import { OrganizationsService } from "@/client"
import { OrganizationActionsMenu } from "@/components/Common/OrganizationActionsMenu"
import AddOrganization from "@/components/Organizations/Add"
import PendingOrganizations from "@/components/Pending/PendingOrganizations"
import {
  PaginationItems,
  PaginationNextTrigger,
  PaginationPrevTrigger,
  PaginationRoot,
} from "@/components/ui/pagination.tsx"

const organizationsSearchSchema = z.object({
  page: z.number().catch(1),
})

const PER_PAGE = 10

function getOrganizationsQueryOptions({ page }: { page: number }) {
  return {
    queryFn: () =>
      OrganizationsService.listOrganizationsRoute({ skip: (page - 1) * PER_PAGE, limit: PER_PAGE }),
    queryKey: ["organizations", { page }],
  }
}

export const Route = createFileRoute("/_auth/_org_layout/orgs/")({
  component: Organizations,
  validateSearch: (search) => organizationsSearchSchema.parse(search),
})

function OrganizationsTable() {
  const navigate = useNavigate({ from: Route.fullPath })
  const { page } = Route.useSearch()

  const { data, isLoading, isPlaceholderData } = useQuery({
    ...getOrganizationsQueryOptions({ page }),
    placeholderData: (prevData) => prevData,
  })

  const setPage = (page: number) =>
    navigate({
      search: (prev: { [key: string]: string }) => ({ ...prev, page }),
    })

  const organizations = data?.data.slice(0, PER_PAGE) ?? []
  const count = data?.count ?? 0

  if (isLoading) {
    return <PendingOrganizations />
  }

  if (organizations.length === 0) {
    return (
      <EmptyState.Root>
        <EmptyState.Content>
          <EmptyState.Indicator>
            <FiSearch />
          </EmptyState.Indicator>
          <VStack textAlign="center">
            <EmptyState.Title>You don't have any organizations yet</EmptyState.Title>
            <EmptyState.Description>
              Add a new organization to get started
            </EmptyState.Description>
          </VStack>
        </EmptyState.Content>
      </EmptyState.Root>
    )
  }

  return (
    <>
      <Table.Root size={{ base: "sm", md: "md" }}>
        <Table.Header>
          <Table.Row>
            <Table.ColumnHeader w="sm">Name</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Description</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Actions</Table.ColumnHeader>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {organizations?.map((organization) => (
            <Table.Row key={organization.id} opacity={isPlaceholderData ? 0.5 : 1}>
              <Table.Cell truncate maxW="sm">
                {organization.display_name}
              </Table.Cell>
              <Table.Cell
                color={!organization.short_description ? "gray" : "inherit"}
                truncate
                maxW="30%"
              >
                {organization.short_description || "N/A"}
              </Table.Cell>
              <Table.Cell>
                <OrganizationActionsMenu organization={organization} />
              </Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table.Root>
      <Flex justifyContent="flex-end" mt={4}>
        <PaginationRoot
          count={count}
          pageSize={PER_PAGE}
          onPageChange={({ page }) => setPage(page)}
        >
          <Flex>
            <PaginationPrevTrigger />
            <PaginationItems />
            <PaginationNextTrigger />
          </Flex>
        </PaginationRoot>
      </Flex>
    </>
  )
}

function Organizations() {
  return (
    <Container maxW="full">
      <Heading size="lg" pt={12}>
        Organizations Management
      </Heading>
      <AddOrganization />
      <OrganizationsTable />
    </Container>
  )
}
