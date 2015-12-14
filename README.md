# openmalaria.tools
This is a set of (command line) tools for end users for usage in combination with the [openMalaria](https://github.com/SwissTPH/openmalaria) simulator program from [SwissTPH](https://github.com/SwissTPH).

No programming experience is required to use these tools.

It contains scripts for
* Plotting openmalaria results with _[plotResults.py](openmalaria/tools/plotResult.py)_
* Generating Schema Documentation from a provided **[schema.xsd](https://github.com/SwissTPH/openmalaria/tree/develop/schema)** with _[generateDoc.py](openmalaria/tools/generateDoc.py)_
* Read Output files  with _[readOutput.py](openmalaria/tools/readOutput.py)_
* Reformat XML files with _[reformat_xmls.py](openmalaria/tools/reformat_xmls.py)_
* translate XML files with _[translateXML.py](openmalaria/tools/translateXML.py)_

Reasons to implement openmalaria.tools as a separate project from vecnet.openmalaria

1. Different license can be used (say user tools can be GPL, while core library can use less restrictive license)
1. openmalaria.tools will have a lot of dependencies on other libraries (lxml, mathlibplot and so on).  vecnet.openmalaria should have as few dependencies as possible - ideally, none.
1. openmalaria.tools is focused on end users, and do not require any programming to be used. vecnet.openmalaria is a library and is intended to be used by python programmers.
1. We may have different versioning approaches for vecnet.openmalaria and openmalaria.tools. For example, the tools may have a version number that tracks the newest OM schema version it supports (e.g., OM Toolkit v33.# supports OM versions up to and including version 33).  In contrast, the vecnet.openmalaria library should use semantic versioning, and only change its major version when there's a backward-incompatible change to its API.

## Tool documentation

Some documentation can be found [in the openmalaria wiki](https://github.com/SwissTPH/openmalaria/wiki/UtilsRunScripts).
