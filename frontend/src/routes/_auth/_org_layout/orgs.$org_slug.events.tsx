import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute(
  '/_auth/_org_layout/orgs/$org_slug/events',
)({
  component: RouteComponent,
})

function RouteComponent() {
  return <div>Hello "/_auth/_org_layout/orgs/$org_slug/events"!</div>
}
