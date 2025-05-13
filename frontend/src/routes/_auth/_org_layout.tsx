import { createFileRoute, Outlet } from '@tanstack/react-router'

export const Route = createFileRoute('/_auth/_org_layout')({
  component: () => <Outlet />,
})