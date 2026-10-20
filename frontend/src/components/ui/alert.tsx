import React from "react"
import { cn } from "@/lib/utils"

export interface AlertProps {
  variant?: "default" | "destructive"
  className?: string
  children: React.ReactNode
}

export const Alert = ({ variant, className, children }: AlertProps) => {
  return (
    <div className={cn(
      "rounded-md p-4",
      variant === "destructive"
        ? "bg-destructive/10 text-destructive"
        : "bg-background/50 text-foreground",
      className,
    )}>
      {children}
    </div>
  )
}