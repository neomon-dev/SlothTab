import React from "react"

export { Button } from "./ui/button"
export { Card } from "./ui/card"
export { Center } from "./ui/center"
export { Heading } from "./ui/heading"
export { Text } from "./ui/text"
export { Spinner } from "./ui/spinner"
export { Input } from "./ui/input"
export { Select } from "./ui/select"
export { Toggle } from "./ui/toggle"
export { Alert } from "./ui/alert"
export { Badge } from "./ui/badge"

export const Box = ({
  className,
  children,
  ...props
}: { className?: string; children?: React.ReactNode; [key: string]: unknown }) => (
  <div className={className} {...(props as React.HTMLAttributes<HTMLDivElement>)}>
    {children}
  </div>
)

export const CardContent = ({
  className,
  children,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={className} {...props}>
    {children}
  </div>
)
