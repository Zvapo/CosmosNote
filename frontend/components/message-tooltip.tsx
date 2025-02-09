import type React from "react"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { SourceData } from "@/lib/types"


interface MessageTooltipProps {
  children: React.ReactNode
  sources?: SourceData[]
}

export function MessageTooltip({ children, sources }: MessageTooltipProps) {
  return (
    <TooltipProvider delayDuration={0}>
      <Tooltip>
        <TooltipTrigger asChild disabled={!!sources?.length}>{children}</TooltipTrigger>

        <TooltipContent side="right" className="w-80 max-h-80 overflow-auto">
          <div className="text-sm space-y-2">
            {sources?.map((source, index) => (
              <div key={index} className="border-b border-border pb-2 last:border-b-0 last:pb-0">
                <a
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-500 hover:underline break-all"
                >
                  {source.url}
                </a>
                <p className="mt-1">{source.content}</p>
              </div>
            ))}
          </div>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  )
}

