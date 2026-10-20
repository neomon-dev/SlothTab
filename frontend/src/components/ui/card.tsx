import React from "react"
import { cn } from "@/lib/utils"

export interface CardProps {
  className?: string
  children: React.ReactNode
}

export const Card = ({ className, children }: CardProps) => {
  return (
    <div className={cn("rounded-lg border border-border bg-card p-6 shadow-sm", className)}>
      {children}
    </div>
  )
}

export const CardContent = ({ className, children }: CardProps) => {
  return <div className={cn("pt-0", className)}>{children}</div>
}