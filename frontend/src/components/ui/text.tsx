import React from "react"
import { cn } from "@/lib/utils"

export const Text = ({ className, children }: { className?: string; children: React.ReactNode; size?: string; mb?: number }) => {
  return <p className={cn("text-sm text-muted-foreground", className)}>{children}</p>
}