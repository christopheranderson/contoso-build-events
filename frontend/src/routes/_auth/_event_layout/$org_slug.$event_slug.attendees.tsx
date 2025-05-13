import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute(
  '/_auth/_event_layout/$org_slug/$event_slug/attendees',
)({
  component: RouteComponent,
})

function RouteComponent() {
  return (
    <div>Hello "/_auth/_event_layout/$org_slug/$event_slug/attendees"!</div>
  )
}
