import {
  Button,
  ButtonGroup,
  DialogActionTrigger,
  Input,
  Text,
  Textarea,
  VStack,
} from "@chakra-ui/react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { type SubmitHandler, useForm } from "react-hook-form"
import { FaExchangeAlt } from "react-icons/fa"

import { type ApiError, type Organization, OrganizationsService, OrganizationUpdate } from "@/client"
import useCustomToast from "@/hooks/useCustomToast"
import { handleError } from "@/utils"
import {
  DialogBody,
  DialogCloseTrigger,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogRoot,
  DialogTitle,
  DialogTrigger,
} from "../ui/dialog"
import { Field } from "../ui/field"

interface EditOrganizationProps {
  organization: Organization
}

const EditOrganization = ({ organization }: EditOrganizationProps) => {
  const [isOpen, setIsOpen] = useState(false)
  const queryClient = useQueryClient()
  const { showSuccessToast } = useCustomToast()
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<OrganizationUpdate>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      ...organization,
    },
  })

  const mutation = useMutation({
    mutationFn: (data: OrganizationUpdate) =>
      OrganizationsService.updateOrganizationRoute({organizationSlug: organization.slug, requestBody: data}),
    onSuccess: () => {
      showSuccessToast("Organization updated successfully.")
      reset()
      setIsOpen(false)
    },
    onError: (err: ApiError) => {
      handleError(err)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["organizations"] })
    },
  })

  const onSubmit: SubmitHandler<OrganizationUpdate> = async (data) => {
    mutation.mutate(data)
  }

  return (
    <DialogRoot
      size={{ base: "xs", md: "md" }}
      placement="center"
      open={isOpen}
      onOpenChange={({ open }) => setIsOpen(open)}
    >
      <DialogTrigger asChild>
        <Button variant="ghost">
          <FaExchangeAlt fontSize="16px" />
          Edit Organization
        </Button>
      </DialogTrigger>
      <DialogContent>
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Edit Organization</DialogTitle>
          </DialogHeader>
          <DialogBody>
            <Text mb={4}>Update the organization details below.</Text>
            <VStack gap={4}>
              <Field
                required
                invalid={!!errors.name}
                errorText={errors.name?.message}
                label="Name"
              >
                <Input
                  id="name"
                  {...register("name", {
                    required: "Name is required",
                  })}
                  placeholder="Name"
                  type="text"
                />
              </Field>

              <Field
                invalid={!!errors.short_description}
                errorText={errors.short_description?.message}
                label="Description"
              >
                <Input
                  id="short_description"
                  {...register("short_description")}
                  placeholder="Enter a short description"
                  type="text"
                />
              </Field>

              <Field
                invalid={!!errors.contact_email}
                errorText={errors.contact_email?.message}
                label="Contact Email"
              >
                <Input
                  id="contact_email"
                  {...register("contact_email")}
                  placeholder="Enter a contact email"
                  type="email"
                />
              </Field>

              <Field
                invalid={!!errors.readme}
                errorText={errors.readme?.message}
                label="Readme"
              >
                <Textarea
                  id="readme"
                  {...register("readme")}
                  placeholder="Enter a readme"
                  autoresize
                />
              </Field>
            </VStack>
          </DialogBody>

          <DialogFooter gap={2}>
            <ButtonGroup>
              <DialogActionTrigger asChild>
                <Button
                  variant="subtle"
                  colorPalette="gray"
                  disabled={isSubmitting}
                >
                  Cancel
                </Button>
              </DialogActionTrigger>
              <Button variant="solid" type="submit" loading={isSubmitting}>
                Save
              </Button>
            </ButtonGroup>
          </DialogFooter>
        </form>
        <DialogCloseTrigger />
      </DialogContent>
    </DialogRoot>
  )
}

export default EditOrganization
