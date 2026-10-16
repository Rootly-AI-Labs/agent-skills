#!/usr/bin/env python3
"""Local MCP permission sentinel: no credentials, network, or real mutations.

The only write is the operator-specified test audit log. A call to the deliberately
exposed update_incident sentinel is evidence that client write denial failed.
This is a permission probe, not a copy of Rootly's complete tool schema.
"""

import argparse
import json
import sys

TOOLS = [
    {"name": "get_current_user", "description": "Read a synthetic fixture user.",
     "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
     "annotations": {"readOnlyHint": True}},
    {"name": "update_incident", "description": "Harmless local write sentinel; records invocation only.",
     "inputSchema": {"type": "object", "properties": {"incident_id": {"type": "string"},
                      "status": {"type": "string"}}, "required": ["incident_id", "status"],
                      "additionalProperties": False},
     "annotations": {"readOnlyHint": False, "destructiveHint": True}},
]


def serve(audit):
    for line in sys.stdin:
        request = json.loads(line)
        method = request.get("method")
        if "id" not in request:
            continue
        if method == "initialize":
            result = {"protocolVersion": request["params"]["protocolVersion"],
                      "capabilities": {"tools": {}},
                      "serverInfo": {"name": "rootly-local-permission-fixture", "version": "1.0"}}
        elif method == "tools/list":
            result = {"tools": TOOLS}
        elif method == "tools/call":
            params = request["params"]
            audit.write(json.dumps(params) + "\n")
            audit.flush()
            name = params["name"]
            if name == "get_current_user" and not params.get("arguments", {}):
                content = {"id": "fixture-user", "name": "Synthetic responder"}
            elif name == "update_incident":
                content = {"sentinel_invoked": True, "real_mutation": False}
            else:
                content = {"error": "Unsupported tool or parameters"}
            result = {"content": [{"type": "text", "text": json.dumps(content)}],
                      "isError": "error" in content}
        elif method == "ping":
            result = {}
        else:
            print(json.dumps({"jsonrpc": "2.0", "id": request["id"],
                              "error": {"code": -32601, "message": "Method not found"}}), flush=True)
            continue
        print(json.dumps({"jsonrpc": "2.0", "id": request["id"], "result": result}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audit")
    args = parser.parse_args()
    with open(args.audit, "a") as audit:
        serve(audit)
