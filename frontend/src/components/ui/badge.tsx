import React from "react"
import { cn } from "@/lib/utils"

export interface BadgeProps {
  variant?: "default" | "secondary" | "destructive" | "outline"
  className?: string
  children: React.ReactNode
}

export const Badge = ({ variant, className, children }: BadgeProps) => {
  return (
    <span className={cn(
      "inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium",
      variant === "default"
        ? "bg-primary/10 text-primary"
        : variant === "secondary"
        ? "bg-secondary/10 text-secondary"
        : variant === "destructive"
        ? "bg-destructive/10 text-destructive"
        : "bg-outline/20 text-outline border border-outline",
      className,
    )}>
      {children}
    </span>
  )
}