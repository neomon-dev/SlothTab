import { cn } from "@/lib/utils"

export interface ToggleProps extends React.ComponentPropsWithoutRef<"button"> {
  type?: "checkbox" | "radio"
}

export const Toggle = React.forwardRef<HTMLButtonElement, ToggleProps>(
  ({ className, type, children, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
      "flex size-4 items-center justify-center rounded-md border-2 border-input bg-transparent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none transition-colors hover:bg-accent hover:text-accent-foreground",
      className,
    )}
      {...props}
      aria-pressed={type === "checkbox"}
      aria-checked={type === "checkbox"}
    >
        {children}
      </button>
    )
  }
)
Toggle.displayName = "Toggle"