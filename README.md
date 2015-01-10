# openmalaria.tools
This is a set of (command line) tools for end users. No programming experience is required to use these tools (although, contributions are welcome)

Reasons to implement openmalaria.tools as a separate project from vecnet.openmalaria

1. Different license can be used (say user tools can be GPL, while core library can use less restrictive license)
2. openmalaria.tools will have a lot of dependencies on other libraries (lxml, mathlibplot and so on).  vecnet.openmalaria should have as few dependencies as possible - ideally, none.
3. openmalaria.tools is focused on end users, and do not require any programming to be used. vecnet.openmalaria is a library and is intended to be used by python programmers.
4. We may have different versioning approaches for vecnet.openmalaria and openmalaria.tools. For example, the tools may have a version number that tracks the newest OM schema version it supports (e.g., OM Toolkit v33.# supports OM versions up to and including version 33).  In contrast, the vecnet.openmalaria library should use semantic versioning, and only change its major version when there's a backward-incompatible change to its API.
