import { Message } from '@/lib/types'
import React from 'react'

interface Props {
    message: Message
}

export default function MessageComponent({ message }: Props) {
    return (
        <div className={`mb-4 flex ${message.role === "user" ? "justify-end" : "justify-start"} max-w-[80%]`}>
            <div
                className={`rounded-lg p-3 ${message.role === "user" ? "bg-primary text-primary-foreground" : "bg-muted"
                    }`}
            >
                {message.content}

                { message.author && (
                    <div className="text-xs text-gray-500 dark:text-gray-400">
                        {message.author}
                    </div>
                )}
            </div>
        </div>
    )
}
