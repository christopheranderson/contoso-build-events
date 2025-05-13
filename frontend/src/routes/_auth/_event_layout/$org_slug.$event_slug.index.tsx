import { Box, Heading, Text, VStack } from '@chakra-ui/react'
import { createFileRoute, useParams } from '@tanstack/react-router'
import { useQuery } from '@tanstack/react-query'
import { EventsService, type Event, EventsReadEventBySlugData } from '@/client'

export const Route = createFileRoute('/_auth/_event_layout/$org_slug/$event_slug/')({
  component: EventIndex,
})

export function EventIndex() {
  const { org_slug, event_slug } = useParams({ strict: false })

  const { data: event, isLoading, error } = useQuery<Event>(
    {
      queryKey: ['event', { org_slug, event_slug }],
      queryFn: () =>
        EventsService.readEventBySlug({
          eventSlug: event_slug,
        }),
    }
  )

  if (isLoading) {
    return <Text>Loading event details...</Text>
  }

  if (error) {
    return <Text>Error loading event details.</Text>
  }

  return (
    <Box p={8}>
      <VStack gap={4} align="start">
        <Heading size="lg">Welcome to {event?.name}</Heading>
        <Text fontSize="md">{event?.short_description}</Text>
        <Text fontSize="sm" color="gray.600">
          {event?.description}
        </Text>
      </VStack>
    </Box>
  )
}