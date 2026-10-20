import { cn } from "@/lib/utils"

export const Center = ({ className, children }: { className?: string; children: React.ReactNode }) => {
  return <div className={cn("flex items-center justify-center", className)}>{children}</div>
}