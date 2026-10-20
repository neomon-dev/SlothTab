import React from "react"
import { cn } from "@/lib/utils"

export const Heading = ({
  className,
  children,
}: { className?: string; children: React.ReactNode; size?: string; mb?: number }) => {
  return <h1 className={cn("text-2xl font-bold mb-2", className)}>{children}</h1>
}