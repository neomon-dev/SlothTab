import React from "react"
import { cn } from "@/lib/utils"

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  asChild?: boolean
  variant?: "primary" | "secondary" | "destructive" | "outline"
  size?: "sm" | "default"
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, children, asChild: _asChild, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none",
          variant === "primary"
            ? "bg-primary text-primary-foreground hover:bg-primary/90"
            : variant === "secondary"
            ? "bg-secondary text-secondary-foreground hover:bg-secondary/80"
            : variant === "destructive"
            ? "bg-destructive text-destructive-foreground hover:bg-destructive/90"
            : "bg-background text-foreground hover:bg-accent",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
          size === "sm" ? "h-8 px-3" : "h-10 px-4",
          className,
        )}
        {...props}
      >
        {children}
      </button>
    )
  }
)
Button.displayName = "Button"