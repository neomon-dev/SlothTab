export { Button } from "./button"
export { Card } from "./card"
export { CardContent } from "./card-content"
export { Center } from "./center"
export { Heading } from "./heading"
export { Text } from "./text"
export { Spinner } from "./spinner"
export { Input } from "./input"
export { Select } from "./select"
export { Toggle } from "./toggle"
export { Alert } from "./alert"
export { Badge } from "./badge"

export const Box = ({
  className,
  children,
  ...props
}: { className?: string; children?: React.ReactNode; [key: string]: unknown }) => (
  <div className={className} {...props}>
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
import React from "react"
