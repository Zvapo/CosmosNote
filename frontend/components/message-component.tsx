import { Message } from '@/lib/types'
import React from 'react'
import { Wrench } from 'lucide-react'
import Markdown from 'react-markdown'
import { MessageTooltip } from './message-tooltip'

interface Props {
    message: Message
}

export default function MessageComponent({ message }: Props) {
    return (
        <div className={`mb-4 flex ${message.role === "user" ? "justify-end" : "justify-start"}`}>

            {message.role === 'tool' ?
                <MessageTooltip sources={message.search_results}>
                <div className="max-w-[80%] rounded-lg p-3 bg-gray-200">
                    <div className="text-sm text-gray-700">
                        <Markdown>{message.content}</Markdown>
                    </div>

                    <div className="text-xs text-gray-500 dark:text-gray-400 flex items-center">
                        <Wrench size={14} className='mr-1' />
                        {message.tool_name}
                    </div>
                </div>
                </MessageTooltip> : (<div
                    className={`max-w-[80%] rounded-lg p-3 ${message.role === "user" ? "bg-primary text-primary-foreground" : "bg-muted"}`}
                >
                    <Markdown>{message.content}</Markdown>

                    {message.author && (
                        <div className="text-xs text-gray-500 dark:text-gray-400">
                            {message.author}
                        </div>
                    )}
                </div>
                )}
        </div>
    )
}
