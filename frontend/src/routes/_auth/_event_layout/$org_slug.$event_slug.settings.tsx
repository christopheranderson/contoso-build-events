import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute(
  '/_auth/_event_layout/$org_slug/$event_slug/settings',
)({
  component: RouteComponent,
})

function RouteComponent() {
  return <div>Not Yet implemented</div>
}
