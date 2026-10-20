import React from "react"
import { cn } from "@/lib/utils"

export const Spinner = ({ className, size = "default", ...props }: { className?: string; size?: "default" | "sm" | "lg"; children?: React.ReactNode; [key: string]: any }) => {
  const sizeClass = size === "sm" ? "h-4 w-4" : size === "lg" ? "h-5 w-5" : "h-5 w-5"
  return (
    <div className={cn("inline-block animate-spin rounded-full h-5 w-5", sizeClass)} {...props} />
  )
}