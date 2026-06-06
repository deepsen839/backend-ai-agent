TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_catalog",
            "description":
                "Search SaaS product catalog",

            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string"
                    }
                },
                "required": [
                    "query"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_user_memory",
            "description":
                "Retrieve user memory",

            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string"
                    }
                },
                "required": [
                    "user_id"
                ]
            }
        }
    }
]